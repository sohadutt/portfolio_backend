from django.urls import path
from . import views

urlpatterns = [
    # JSON / Database Reading Endpoints
    path('all/', views.JobviewAll.as_view(), name='job-all'),
    path('matched/', views.JobviewMatched.as_view(), name='job-matched'),

    # Signal endpoints (Triggers the Celery task)
    path('signals/start/<str:site_name>/', views.SignalStart.as_view(), name='start-job-signal'),
]