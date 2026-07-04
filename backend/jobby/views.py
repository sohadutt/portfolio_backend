from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from django.db import transaction
from django.db.models import F
from django.http import Http404

from portfolio_form.tasks import run_job_pipeline
from portfolio_form.models import PortfolioSettings, User

from .models import Job, PortfolioJobMatch
from .serializers import JobSerializer, PortfolioJobMatchSerializer


def _query_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@transaction.atomic
def _consume_analysis_credit(user: User) -> tuple[bool, int]:
    locked_user = User.objects.select_for_update().get(pk=user.pk)
    if locked_user.job_analysis_limit <= 0:
        return False, 0

    locked_user.job_analysis_limit -= 1
    locked_user.save(update_fields=["job_analysis_limit"])
    return True, locked_user.job_analysis_limit


def _refund_analysis_credit(user_id: int) -> None:
    User.objects.filter(pk=user_id).update(job_analysis_limit=F("job_analysis_limit") + 1)

class SignalStart(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def post(self, request: Request, site_name: str):
        try:
            order_index = int(request.query_params.get("order_index", 1))
        except ValueError:
            order_index = 1

        match_only_param = _query_bool(request.query_params.get('match_only'), False)
        run_scraper_param = _query_bool(request.query_params.get('scraper'), True)
        run_processor_param = _query_bool(request.query_params.get('processor'), True)
        if match_only_param:
            run_scraper_param = False
            run_processor_param = True

        user = request.user
        try:
            portfolio = PortfolioSettings.objects.get(
                owner=user, order_index=order_index, is_enabled=True, owner__tier=2
            )
        except PortfolioSettings.DoesNotExist:
            try:
                portfolio = PortfolioSettings.objects.get(
                    owner=user, order_index=1, is_enabled=True, owner__tier=2
                )
            except PortfolioSettings.DoesNotExist:
                raise Http404("No enabled portfolios found for this user. or the user is not a premium user.")

        should_consume_credit = run_processor_param or match_only_param
        remaining_credits = user.job_analysis_limit
        if should_consume_credit:
            has_credit, remaining_credits = _consume_analysis_credit(user)
            if not has_credit:
                return Response(
                    {"error": "No credit left for analysis.", "job_analysis_limit": 0},
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )
        
        try:
            task = run_job_pipeline.delay(site_name, run_scraper_param, run_processor_param, portfolio.id, match_only_param)
            return Response(
                {
                    "message": "Job pipeline started successfully.",
                    "task_id": task.id,
                    "match_only": match_only_param,
                    "job_analysis_limit": remaining_credits,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            if should_consume_credit:
                _refund_analysis_credit(user.id)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobAnalysisCreditView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        request.user.refresh_from_db(fields=["job_analysis_limit"])
        return Response({"job analysis limit": request.user.job_analysis_limit})


class JobviewAll(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        user = User.objects.get(pk=request.user.pk)
        per_page = request.query_params.get('per_page', 20)
        if user.tier < 2:
            return Response(
                {"error": "User does not have access to this endpoint."},
                status=status.HTTP_403_FORBIDDEN,
            )
        site_name = request.query_params.get('site_name', None)
        enriched_only = _query_bool(request.query_params.get('enriched_only'), False)
        
        jobs_query = Job.objects.all()
        if site_name:
            jobs_query = Job.objects.filter(platform_name__icontains=site_name)
        if enriched_only:
            jobs_query = Job.objects.exclude(tags=[])
            
        paginator = PageNumberPagination()
        paginator.page_size = int(per_page)
        paginated_jobs = paginator.paginate_queryset(jobs_query, request)
        
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)


class JobviewMatched(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        site_name = request.query_params.get('site_name', None)
        per_page = request.query_params.get('per_page', 20)
        try:
            order_index = int(request.query_params.get("order_index", 0))
        except ValueError:
            order_index = 0
        try:
            min_score = float(request.query_params.get("min_score", 0))
        except ValueError:
            min_score = 0
        user = request.user
        
        matches_query = PortfolioJobMatch.objects.filter(portfolio__owner=user).select_related('job')
        
        if site_name:
            matches_query = matches_query.filter(job__platform_name__icontains=site_name)
        if order_index:
            matches_query = matches_query.filter(portfolio__order_index=order_index)
        if min_score:
            matches_query = matches_query.filter(match_score__gte=min_score)
            
        paginator = PageNumberPagination()
        paginator.page_size = int(per_page)
        paginated_matches = paginator.paginate_queryset(matches_query, request)
        
        serializer = PortfolioJobMatchSerializer(paginated_matches, many=True)
        return paginator.get_paginated_response(serializer.data)

class JobFilterView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        user = User.objects.get(pk=request.user.pk)
        if user.tier < 2:
            return Response(
                {"error": "User does not have access to this endpoint."},
                status=status.HTTP_403_FORBIDDEN,
            )
        site_name = request.query_params.get('site_name', None)
        enriched_only = _query_bool(request.query_params.get('enriched_only'), False)
        per_page = request.query_params.get('per_page', 20)
        
        jobs_query = Job.objects.all()
        if site_name:
            jobs_query = Job.objects.filter(platform_name__icontains=site_name)
        if enriched_only:
            jobs_query = Job.objects.exclude(tags=[])
            
        paginator = PageNumberPagination()
        paginator.page_size = int(per_page)
        paginated_jobs = paginator.paginate_queryset(jobs_query, request)
        
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)