from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("csrf/", views.csrf_token, name="csrf_token"),
    path("profiles/", views.create_profile, name="create_profile"),
    path("auth/login/", views.login, name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/tokens/", views.profile_tokens, name="profile_tokens"),
    path("shares/<str:token>/submissions/", views.submit_form, name="submit_form"),
    path("submissions/", views.list_submissions, name="list_submissions"),
    path("submissions/<int:form_id>/", views.update_submission, name="update_submission"),
]
