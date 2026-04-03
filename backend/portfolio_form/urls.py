from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from . import views

urlpatterns = [
    path("csrf/", views.get_csrf_token, name="csrf_token"),
    path("portfolio/",views.get_default_public_portfolio,name="default_public_portfolio",),
    path("portfolio/<str:share_token>/",views.get_shared_public_portfolio,name="shared_public_portfolio",),
    path("profiles/create/", views.create_user_profile, name="create_user_profile"),
    path("profiles/", views.create_user_profile, name="create_user_profile_v2"),
    path("form_submit/",views.submit_mail_default_portfolio,name="submit mail to the default user 1",),
    path("shares/<str:share_token>/submissions/",views.submit_mail_public_portfolio,name="share_submissions",),
    path("<str:share_token>/form_submit/",views.submit_mail_public_portfolio,name="submit_mail_public_portfolio",),
    path("auth/login/", views.login_user, name="login_user"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="token_logout"),
    path("profiles/tokens/", views.get_profile_tokens, name="get_profile_tokens"),
    path("profile/tokens/", views.get_profile_tokens, name="get_profile_tokens_v2"),
    path("mails/",views.list_dashboard_submissions,name="list_dashboard_submissions",),
    path("submissions/",views.list_dashboard_submissions,name="list_dashboard_submissions_v2",),
    path("mails/reorder/",views.reorder_dashboard_submissions,name="reorder_dashboard_submissions",),
    path("submissions/reorder/",views.reorder_dashboard_submissions,name="reorder_dashboard_submissions_v2",),
    path("mails/<int:form_id>/",views.update_dashboard_submission,name="update_dashboard_submission",),
    path("submissions/<int:form_id>/",views.update_dashboard_submission,name="update_dashboard_submission_v2",),
]
