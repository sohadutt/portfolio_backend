from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from . import views

urlpatterns = [
    # Profile & Authentication
    path("csrf/", views.get_csrf_token, name="csrf_token"), # Fixed: Removed leading slash
    path("profile/", views.get_user_profile, name="get_user_profile"),
    path("profile/register/", views.create_user_profile, name="create_user_profile"),
    path("profile/login/", views.login_user, name="login_user"),
    path("profile/auth-otp/", views.auth_otp, name="auth_otp"),
    path("profile/verify-otp/", views.verify_otp, name="verify_otp"),    
    
    path("profile/share-toggle/", views.status_share_token, name="status_share_token"),
    
    path("profile/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/logout/", TokenBlacklistView.as_view(), name="token_logout"),
    path("profile/tokens/", views.get_profile_tokens, name="get_profile_tokens"),

    # Public Portfolios (Viewing)
    path("portfolio/", views.get_default_public_portfolio, name="default_public_portfolio"),
    path("portfolio/shared/<str:share_token>/", views.get_shared_public_portfolio, name="shared_public_portfolio"),

    # Portfolio Management (Authenticated)
    path("portfolio/create/", views.submit_portfolio, name="submit_portfolio"),
    path("portfolio/update/", views.update_portfolio, name="update_portfolio"),

    # Public Form Submissions (Visitors contacting owners)
    path("forms/submit/", views.submit_mail_default_portfolio, name="submit_default_portfolio_mail"),
    path("forms/shared/<str:share_token>/submit/", views.submit_mail_public_portfolio, name="share_submissions"),

    # Dashboard Management
    path("dashboard/submissions/", views.list_dashboard_submissions, name="list_dashboard_submissions"),
    path("dashboard/submissions/reorder/", views.reorder_dashboard_submissions, name="reorder_dashboard_submissions"),
    path("dashboard/submissions/<int:form_id>/", views.update_dashboard_submission, name="update_dashboard_submission"),
]