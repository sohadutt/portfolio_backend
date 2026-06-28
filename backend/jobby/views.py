from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from jobby import JobManager

class SignalStart(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]
    job_manager = JobManager()

    def post(self, request: Request, site_name: str):
        try:
            self.job_manager.process_jobs(site_name=site_name)
            
        except Exception as e:
            print(f"Error processing job data: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "Job data received successfully.", "data": {}}, status=status.HTTP_200_OK)

class JobviewAll(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        jobs = []
        paginator = PageNumberPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        return paginator.get_paginated_response(paginated_jobs)

class JobviewMatched(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        matched_jobs = []
        paginator = PageNumberPagination()
        paginated_jobs = paginator.paginate_queryset(matched_jobs, request)
        return paginator.get_paginated_response(paginated_jobs)
