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
    path("profile/get-token/", views.get_profile_tokens, name="profile_token"),

    # --- Public Portfolio Viewing ---
    # Default User Routes
    path("portfolio/default/", views.get_default_public_portfolio, {"order_index": 1}, name="portfolio_default_primary"),
    path("portfolio/default/<int:order_index>/", views.get_default_public_portfolio, name="portfolio_default_indexed"),
    
    # Shared Token Routes
    path("portfolio/shared/<str:share_token>/", views.get_shared_public_portfolio, {"order_index": 1}, name="portfolio_shared_primary"),
    path("portfolio/shared/<str:share_token>/<int:order_index>/", views.get_shared_public_portfolio, name="portfolio_shared_indexed"),

    # --- Portfolio Content Management (Authenticated) ---
    path("portfolio/submit/<int:order_index>/", views.submit_portfolio, name="portfolio_submit_indexed"), 
    path("portfolio/update/<int:order_index>/", views.update_portfolio, name="portfolio_update_indexed"),

    # --- Contact Form & Submissions ---
    # Public endpoints for visitors
    path("forms/submit/default/<int:order_index>/", views.submit_mail_default_portfolio, name="form_submit_default_indexed"),
    path("forms/submit/shared/<str:share_token>/", views.submit_mail_public_portfolio, {"order_index": 1}, name="form_submit_shared_primary"),

    # --- Dashboard Management (Authenticated) ---
    # Submissions
    path("dashboard/submissions/view/", views.list_dashboard_submissions, name="dashboard_submissions_list"),
    path("dashboard/submissions/update/<int:form_id>/", views.update_dashboard_submission, name="dashboard_submission_update"),
    path("dashboard/submissions/reorder/", views.reorder_dashboard_submissions, name="dashboard_submissions_reorder"),
    
    # Portfolios
    path("dashboard/portfolios/<int:order_index>/toggle/", views.toggle_portfolio_status, name="dashboard_portfolio_toggle"),
    path("dashboard/portfolios/all/", views.preview_all_portfolios, name="dashboard_all_portfolios"),

    # --- Admin & External Triggers ---
    # Secure webhook for external cron job (cron-job.org / UptimeRobot)
    path("cron/cleanup/", views.trigger_user_cleanup, name="cron_cleanup"),
    path("cron/urgent-notifications/", views.trigger_urgent_notifications, name="cron_urgent_notifications"),
]