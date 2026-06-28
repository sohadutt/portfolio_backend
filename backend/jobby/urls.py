from django.urls import path
from . import views

urlpatterns = [
    path('jobs/{?user_id=<int:user_id>}/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),

    # Signal endpoints
    path('signals/start/<str:site_name>/', views.SignalStart.as_view(), name='start-job-signal'),
    
]