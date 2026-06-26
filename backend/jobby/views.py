from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import APIView, api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle



class JobListView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def get(self, request: Request):
        jobs = [] 
        paginator = PageNumberPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        return paginator.get_paginated_response(paginated_jobs)
