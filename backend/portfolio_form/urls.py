from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from . import views

urlpatterns = [
    path("csrf", views.get_csrf_token, name="csrf_token"),
    path("auth/login", views.login_user, name="login_user"),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout", TokenBlacklistView.as_view(), name="token_logout"),
    path("profiles", views.create_user_profile, name="create_user_profile"),
    path("profile/tokens", views.get_profile_tokens, name="get_profile_tokens"),
    path("portfolio", views.get_default_public_portfolio, name="default_public_portfolio"),
    path("portfolio/<str:share_token>", views.get_shared_public_portfolio, name="shared_public_portfolio"),
    path("portfolio/submit", views.submit_portfolio, name="submit_portfolio"),
    path("portfolio/update", views.update_portfolio, name="update_portfolio"),
    path("forms/submit", views.submit_mail_default_portfolio, name="submit_default_portfolio_mail"),
    path("forms/submit/<str:share_token>", views.submit_mail_public_portfolio, name="share_submissions"),
    path("forms/submissions", views.list_dashboard_submissions, name="list_dashboard_submissions"),
    path("forms/submissions/reorder", views.reorder_dashboard_submissions, name="reorder_dashboard_submissions"),
    path("forms/submissions/<int:form_id>", views.update_dashboard_submission, name="update_dashboard_submission"),
]
