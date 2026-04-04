from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from . import views

urlpatterns = [
    # --- Authentication & Security ---
    path("csrf/", views.get_csrf_token, name="csrf_token"),
    path("auth/register/", views.create_user_profile, name="auth_register"),
    path("auth/login/", views.login_user, name="auth_login"),
    path("auth/otp/request/", views.auth_otp, name="auth_otp_request"),
    path("auth/otp/verify/", views.verify_otp, name="auth_otp_verify"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="token_logout"),

    # --- User Profile Management ---
    path("profile/", views.get_user_profile, name="profile_get"),
    path("profile/update/", views.update_user_profile, name="profile_update"),
    path("profile/share-toggle/", views.status_share_token, name="profile_share_toggle"),
    path("profile/tokens/", views.get_profile_tokens, name="profile_tokens"),

    # --- Public Portfolio Viewing ---
    path("portfolio/default/", views.get_default_public_portfolio, name="portfolio_public_default"),
    path("portfolio/shared/<str:share_token>/", views.get_shared_public_portfolio, name="portfolio_public_shared"),

    # --- Portfolio Content Management (Authenticated) ---
    path("portfolio/save/", views.submit_portfolio, name="portfolio_save"), 
    # Note: submit_portfolio handles both create and update (partial) in your optimized views

    # --- Contact Form & Submissions ---
    # Public endpoints for visitors
    path("forms/submit/default/", views.submit_mail_default_portfolio, name="form_submit_default"),
    path("forms/submit/shared/<str:share_token>/", views.submit_mail_public_portfolio, name="form_submit_shared"),

    # Dashboard endpoints for owners
    path("dashboard/submissions/", views.list_dashboard_submissions, name="dashboard_submissions_list"),
    path("dashboard/submissions/<int:form_id>/", views.update_dashboard_submission, name="dashboard_submission_update"),
    path("dashboard/submissions/reorder/", views.reorder_dashboard_submissions, name="dashboard_submissions_reorder"),
]