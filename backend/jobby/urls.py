from django.urls import path
from . import views

urlpatterns = [
    # General job list and detail (Assuming you still have these views defined)
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),

    # JSON File Reading Endpoints
    path('jobs/all/', views.JobviewAll.as_view(), name='job-all'),
    path('jobs/matched/', views.JobviewMatched.as_view(), name='job-matched'),

    # Signal endpoints (Triggers the Celery task)
    path('signals/start/<str:site_name>/', views.SignalStart.as_view(), name='start-job-signal'),
]