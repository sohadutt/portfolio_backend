from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.JobviewAll.as_view(), name='job-all'),
    path('matched/', views.JobviewMatched.as_view(), name='job-matched'),
    path('credits/', views.JobAnalysisCreditView.as_view(), name='job-analysis-credits'),
    path('search/<bool:enriched_only>/<str:site_name>/', views.JobFilterView.as_view(), name='job-search'),

    # Signal endpoints (Triggers the Celery task)
    path('signals/start/<str:site_name>/', views.SignalStart.as_view(), name='start-job-signal'),
]
