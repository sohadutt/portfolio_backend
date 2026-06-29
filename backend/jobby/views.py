from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from django.http import Http404

from portfolio_form.tasks import run_job_pipeline
from portfolio_form.models import PortfolioSettings

from .models import Job, PortfolioJobMatch
from .serializers import JobSerializer, PortfolioJobMatchSerializer

class SignalStart(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def post(self, request: Request, site_name: str):
        try:
            order_index = int(request.query_params.get("order_index", 1))
        except ValueError:
            order_index = 1

        run_scraper_param = request.query_params.get('scraper', 'true').lower() == 'true'
        run_processor_param = request.query_params.get('processor', 'true').lower() == 'true'
        user = request.user
        
        try:
            portfolio = PortfolioSettings.objects.get(
                owner=user, order_index=order_index, is_enabled=True
            )
        except PortfolioSettings.DoesNotExist:
            try:
                portfolio = PortfolioSettings.objects.get(
                    owner=user, order_index=1, is_enabled=True
                )
            except PortfolioSettings.DoesNotExist:
                raise Http404("No enabled portfolios found for this user.")
        
        try:
            task = run_job_pipeline.delay(site_name, run_scraper_param, run_processor_param, portfolio.id)
            return Response({"message": "Job pipeline started successfully.", "task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobviewAll(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        site_name = request.query_params.get('site_name', None)
        
        jobs_query = Job.objects.all()
        if site_name:
            jobs_query = jobs_query.filter(platform_name__iexact=site_name)
            
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_jobs = paginator.paginate_queryset(jobs_query, request)
        
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)


class JobviewMatched(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        site_name = request.query_params.get('site_name', None)
        user = request.user
        
        matches_query = PortfolioJobMatch.objects.filter(portfolio__owner=user).select_related('job')
        
        if site_name:
            matches_query = matches_query.filter(job__platform_name__iexact=site_name)
            
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_matches = paginator.paginate_queryset(matches_query, request)
        
        serializer = PortfolioJobMatchSerializer(paginated_matches, many=True)
        return paginator.get_paginated_response(serializer.data)