from __future__ import annotations

import os
import re
import time
import secrets
import tempfile
import requests
import random
from typing import Any

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes, throttle_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle

from .utils import compress_to_webp
from .tasks import (
    send_otp_email_task, 
    cleanup_unverified_users, 
    process_daily_urgent_notifications,
    async_upload_profile_picture, 
    async_upload_resume
)
from .models import (
    ContactFormSubmission, Experience, FeaturedModule, HeroMetric, 
    Link, PortfolioSettings, Project, ShowcaseCategory, SkillGroup, User
)
from .serializers import (
    LoginSerializer, PortfolioSubmissionSerializer, ProfileCreateSerializer,
    serialize_portfolio_payload,
    SubmissionCreateSerializer, SubmissionReadSerializer, SubmissionReorderSerializer,
    SubmissionUpdateSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class for listing dashboard submissions."""
    page_size: int = 10
    page_size_query_param: str = 'page_size'
    max_page_size: int = 40

@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request: Request) -> Response:
    """Sets the CSRF cookie for frontend clients."""
    return Response({"detail": "CSRF cookie set"})

def get_request_ip(request: Request) -> str | None:
    """Extracts the real client IP address from the request headers."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR")

def generate_username_from_email(email: str) -> str:
    """Generates a unique username based on the user's email prefix."""
    base = re.sub(r"[^a-z0-9._+-]", "", email.split("@")[0].lower()) or "user"
    username, suffix = base, 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{suffix}"
        suffix += 1
    return username

@api_view(["POST"])
@permission_classes([AllowAny])
def create_user_profile(request: Request) -> Response:
    """Registers a new user, sets them as unverified, and triggers an OTP email."""
    email = str(request.data.get("email", "")).strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response({"message": "Email and password required."}, status=400)

    serializer = ProfileCreateSerializer(data={
        "email": email, "password": password, "username": generate_username_from_email(email)
    })
    
    if not serializer.is_valid():
        return Response({"message": "Registration failed.", "errors": serializer.errors}, status=400)

    user = serializer.save()
    otp = ''.join(secrets.choice('0123456789') for _ in range(6))
    cache.set(f"otp:{email}", otp, timeout=200)

    try:
        send_otp_email_task.delay(email, otp)
        status_msg = "OTP sent to your email."
    except Exception:
        status_msg = "Email service error. Please log in to resend."

    return Response({"message": f"Profile created. {status_msg}", "data": {"user_id": user.id, "email": user.email}}, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def auth_otp(request: Request) -> Response:
    """Requests a new OTP for an existing unverified user. Includes timing protection to prevent email enumeration."""
    email = str(request.data.get("email", "")).strip().lower()
    user = User.objects.filter(email=email).first()

    if not user:
        time.sleep(random.uniform(0.1, 0.3)) 
    else:
        otp = ''.join(secrets.choice('0123456789') for _ in range(6))
        cache.set(f"otp:{email}", otp, timeout=200)
        try:
            send_otp_email_task.delay(email, otp)
        except Exception: pass

    return Response({"message": "If an account exists, an OTP will be sent shortly."})

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp(request: Request) -> Response:
    """Validates the OTP and marks the user account as verified."""
    email = str(request.data.get("email", "")).strip().lower()
    otp_provided = str(request.data.get("otp", "")).strip()

    if cache.get(f"otp:{email}") != otp_provided:
        return Response({"message": "Invalid or expired OTP."}, status=400)

    user = get_object_or_404(User, email=email)
    if not user.is_verified:
        user.is_verified = True
        user.save()

    cache.delete(f"otp:{email}")
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "message": "OTP verified.",
        "data": {"user_id": user.id, "email": user.email, "username": user.username},
        "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request: Request) -> Response:
    """Authenticates a user via email/password and returns JWT tokens."""
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    
    if not user.is_verified:
        return Response({"message": "Verification required."}, status=403)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        "message": "Login successful",
        "data": {
            "user_id": user.id, "email": user.email, "username": user.username,
            "enable_share_token": user.enable_share_token, "share_token": user.share_token,
            "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}
        }
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def google_login(request: Request) -> Response:
    """Handles Google OAuth login/registration. Automatically verifies accounts created this way."""
    token = request.data.get("credential") or request.data.get("token")
    
    if not token:
        return Response({"message": "Google token required."}, status=400)
        
    try:
        google_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if not google_response.ok:
            return Response({"message": "Invalid or expired Google token."}, status=403)
            
        id_info = google_response.json()
        email = id_info.get("email")
        
        if not email:
            return Response({"message": "Google token invalid: No email provided."}, status=400)
        
        user, created = User.objects.get_or_create(email=email, defaults={
            "username": generate_username_from_email(email),
            "first_name": id_info.get("given_name", ""),
            "last_name": id_info.get("family_name", ""),
            "is_verified": True
        })
        
        if not created and not user.is_verified:
            user.is_verified = True
            user.save(update_fields=['is_verified'])
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Login successful",
            "data": {
                "user_id": user.id, 
                "email": user.email, 
                "username": user.username,
                "enable_share_token": user.enable_share_token, 
                "share_token": user.share_token,
                "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)}
            }
        })
        
    except Exception as e:
        return Response({"message": f"Authentication failed: {str(e)}"}, status=500)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request: Request) -> Response:
    """Fetches the authenticated user's profile metadata and tier settings."""
    u = request.user
    return Response({
        "user_id": u.id, "email": u.email, "username": u.username,
        "first_name": u.first_name, "last_name": u.last_name,
        "profile_picture": u.profile_picture_url,
        "theme_mode": u.theme_mode,
        "tier": u.tier,
        "portfolio_count": PortfolioSettings.objects.filter(owner=u).count(),
        "is_verified": u.is_verified, "enable_share_token": u.enable_share_token,
        "share_token": u.share_token if (u.is_verified and u.enable_share_token) else None
    })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_user_profile(request: Request) -> Response:
    """
    Updates user settings. If a profile picture is provided, it processes 
    and dispatches the upload to a background Celery task.
    """
    user = request.user
    
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)

    if "theme_mode" in request.data:
        try:
            user.theme_mode = int(request.data.get("theme_mode"))
        except (ValueError, TypeError):
            return Response({"error": "theme_mode must be an integer."}, status=400)

    is_uploading_image = False

    if "profile_picture" in request.FILES:
        old_url = user.profile_picture_url
        original_file = request.FILES["profile_picture"]
        
        try:
            # Compress the image locally
            webp_file = compress_to_webp(original_file)
            webp_file.seek(0)
            
            random_suffix = secrets.token_hex(3)
            filename = f"u{user.id}_{random_suffix}.webp"
            
            # Write to a secure temporary file for the Celery worker to pick up
            fd, temp_path = tempfile.mkstemp(suffix=".webp", prefix=f"u{user.id}_")
            with os.fdopen(fd, 'wb') as f:
                f.write(webp_file.read())
            
            os.chmod(temp_path, 0o644) 
            
            # Dispatch to background task
            async_upload_profile_picture.delay(user.id, temp_path, filename, old_url)
            is_uploading_image = True

        except Exception as e:
            return Response({"error": f"Upload preparation failed: {str(e)}"}, status=500)
            
    user.save()

    msg = "Profile updated successfully."
    if is_uploading_image:
        msg += " Your profile picture is uploading in the background."

    return Response({
        "message": msg, 
        "data": {
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "theme_mode": user.theme_mode,
            "profile_picture": str(user.profile_picture_url) if user.profile_picture_url else None,
        }
    })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def status_share_token(request: Request) -> Response:
    """Toggles the public visibility (share token) of the user's portfolios."""
    user = request.user
    if not user.is_verified:
        return Response({"message": "Verify email to enable sharing."}, status=403)

    if "enable_share_token" in request.data:
        val = request.data.get("enable_share_token")
        user.enable_share_token = str(val).lower() in ['true', '1', 't'] if isinstance(val, str) else bool(val)
    else:
        user.enable_share_token = not user.enable_share_token
        
    user.save(update_fields=["enable_share_token"])
    
    return Response({
        "enable_share_token": user.enable_share_token,
        "share_token": user.share_token if user.enable_share_token else None
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_tokens(request: Request) -> Response:
    """Returns the user's current share token status and string."""
    return Response({
        "enable_share_token": request.user.enable_share_token,
        "share_token": request.user.share_token,
    })

def serialize_portfolio_data(portfolio: PortfolioSettings, request: Request | None = None) -> dict[str, Any]:
    """Helper to attach user tier and theme mode to the portfolio payload."""
    data = serialize_portfolio_payload(portfolio)
    data["tier"] = portfolio.tier
    data["themeMode"] = portfolio.owner.theme_mode
    return data

@api_view(["GET"])
@permission_classes([AllowAny])
def get_default_public_portfolio(request: Request) -> Response:
    """Fetches the platform's primary default portfolio (User ID 1) with optimized prefetching."""
    try:
        order_index = int(request.query_params.get("order_index", 1))
    except ValueError:
        order_index = 1
        
    owner = User.objects.filter(id=1).first() or User.objects.order_by('id').first()
    if not owner: 
        raise Http404()
        
    # NOTE: Ensure serializers.py is updated to use .all() instead of .filter() to fully utilize prefetch
    prefetch_relations = [
        'herometrics', 'skillgroups', 'projects', 'experiences', 
        'showcasecategorys', 'featuredmodules', 'links'
    ]
    
    try:
        portfolio = PortfolioSettings.objects.prefetch_related(*prefetch_relations).get(
            owner=owner, order_index=order_index, is_enabled=True
        )
    except PortfolioSettings.DoesNotExist:
        try:
            portfolio = PortfolioSettings.objects.prefetch_related(*prefetch_relations).get(
                owner=owner, order_index=1, is_enabled=True
            )
        except PortfolioSettings.DoesNotExist:
            raise Http404("No enabled portfolios found for this user.")
            
    return Response(serialize_portfolio_data(portfolio, request))

@api_view(["GET"])
@permission_classes([AllowAny])
def get_shared_public_portfolio(request: Request, share_token: str) -> Response:
    """Fetches a specific user's public portfolio by share token with optimized prefetching."""
    try:
        order_index = int(request.query_params.get("order_index", 1))
    except ValueError:
        order_index = 1        
        
    owner = get_object_or_404(User, share_token=share_token, enable_share_token=True)    
    
    prefetch_relations = [
        'herometrics', 'skillgroups', 'projects', 'experiences', 
        'showcasecategorys', 'featuredmodules', 'links'
    ]
    
    try:
        portfolio = PortfolioSettings.objects.prefetch_related(*prefetch_relations).get(
            owner=owner, order_index=order_index, is_enabled=True
        )
    except PortfolioSettings.DoesNotExist:
        try:
            portfolio = PortfolioSettings.objects.prefetch_related(*prefetch_relations).get(
                owner=owner, order_index=1, is_enabled=True
            )
        except PortfolioSettings.DoesNotExist:
            raise Http404("No enabled portfolios found for this user.")         
            
    return Response(serialize_portfolio_data(portfolio, request))

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_portfolio_authenticated(request: Request, order_index: int = 1) -> Response:
    """Fetches the authenticated user's own portfolio data for dashboard editing."""
    prefetch_relations = [
        'herometrics', 'skillgroups', 'projects', 'experiences', 
        'showcasecategorys', 'featuredmodules', 'links'
    ]
    portfolio = get_object_or_404(
        PortfolioSettings.objects.prefetch_related(*prefetch_relations), 
        owner=request.user, 
        order_index=order_index
    )
    return Response(serialize_portfolio_data(portfolio, request))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def submit_portfolio(request: Request, order_index: int = 1) -> Response:
    """Creates a new portfolio. Dispatches resume uploads to a background Celery worker."""
    if not request.user.is_verified:
        return Response({"message": "Verify first."}, status=403)
        
    if int(order_index) > 1 and request.user.tier == User.Tier.FREE:
        return Response({"message": "Upgrade to Premium to create multiple portfolios."}, status=403)
    
    data = request.data.copy()
    resume_temp_path = None
    resume_filename = None

    if "resume" in request.FILES:
        try:
            resume_file = request.FILES["resume"]
            random_suffix = secrets.token_hex(3)
            resume_filename = f"resume_{random_suffix}.pdf"
            
            fd, resume_temp_path = tempfile.mkstemp(suffix=".pdf", prefix="resume_")
            with os.fdopen(fd, 'wb') as f:
                for chunk in resume_file.chunks():
                    f.write(chunk)
            
            os.chmod(resume_temp_path, 0o644)
            
        except Exception as e:
            return Response({"message": f"Resume preparation failed: {str(e)}"}, status=500)

    serializer = PortfolioSubmissionSerializer(data=data, context={"owner": request.user, "order_index": order_index})
    serializer.is_valid(raise_exception=True)
    portfolio = serializer.save(owner=request.user)

    is_uploading_resume = False
    if resume_temp_path and resume_filename:
        # Dispatch to background task
        async_upload_resume.delay(portfolio.id, resume_temp_path, resume_filename, portfolio.resume_url)
        is_uploading_resume = True

    msg = "Portfolio saved."
    if is_uploading_resume:
        msg += " Your resume is uploading in the background."

    return Response({
        "message": msg, 
        "data": serialize_portfolio_data(portfolio)
    })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def update_portfolio(request: Request, order_index: int = 1) -> Response:
    """Updates portfolio data. Uses transaction.atomic to ensure index shifts don't corrupt data."""
    if not request.user.is_verified:
        return Response({"message": "Verify first."}, status=403)
        
    new_order_index = request.data.get("new_order_index")
    is_enabled = request.data.get("is_enabled")
    
    if "personalInfo" not in request.data and (new_order_index is not None or is_enabled is not None):
        portfolio = get_object_or_404(PortfolioSettings, owner=request.user, order_index=order_index)
        updated = False
        
        if new_order_index and int(new_order_index) != int(order_index):
            if int(new_order_index) > 1 and request.user.tier == User.Tier.FREE:
                return Response({"message": "Upgrade to Premium to create multiple portfolios."}, status=403)
            portfolio.move_to_index(int(new_order_index))
            updated = True
            
        if is_enabled is not None:
            if bool(is_enabled) and portfolio.order_index > 1 and request.user.tier == User.Tier.FREE:
                 return Response({"message": "Upgrade to Premium to enable multiple portfolios."}, status=403)
            portfolio.is_enabled = bool(is_enabled)
            portfolio.save(update_fields=['is_enabled'])
            updated = True
            
        if updated:
            portfolio.refresh_from_db()
            return Response({
                "message": "Portfolio settings updated.", 
                "data": serialize_portfolio_data(portfolio)
            })

    if int(order_index) > 1 and request.user.tier == User.Tier.FREE:
        return Response({"message": "Upgrade to Premium to create multiple portfolios."}, status=403)

    serializer = PortfolioSubmissionSerializer(
        data=request.data, 
        context={"owner": request.user, "order_index": order_index},
        partial=True
    )
    serializer.is_valid(raise_exception=True)
    portfolio = serializer.save(owner=request.user)

    if new_order_index and int(new_order_index) != int(order_index):
        if int(new_order_index) > 1 and request.user.tier == User.Tier.FREE:
             return Response({"message": "Saved data, but upgrade to Premium to shift portfolio indices."}, status=403)
        portfolio.move_to_index(int(new_order_index))
        portfolio.refresh_from_db()

    return Response({"message": "Portfolio updated.", "data": serialize_portfolio_data(portfolio)})

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def toggle_portfolio_status(request: Request, order_index: int) -> Response:
    """Quick toggle to enable or disable a specific portfolio."""
    portfolio = get_object_or_404(PortfolioSettings, owner=request.user, order_index=order_index)
    
    if not portfolio.is_enabled:
        if portfolio.order_index > 1 and request.user.tier == User.Tier.FREE:
            return Response({"message": "Upgrade to Premium to enable multiple portfolios."}, status=403)
            
    portfolio.is_enabled = not portfolio.is_enabled
    portfolio.save(update_fields=['is_enabled'])
    
    status_text = "enabled" if portfolio.is_enabled else "disabled"
    
    return Response({
        "message": f"Portfolio {order_index} is now {status_text}.", 
        "is_enabled": portfolio.is_enabled
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_dashboard_submissions(request: Request) -> Response:
    """Lists all contact form submissions sent to the authenticated user, paginated."""
    subs = ContactFormSubmission.objects.filter(owner=request.user).order_by('-submitted_at')
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(subs, request)
    if page is not None:
        serializer = SubmissionReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    serializer = SubmissionReadSerializer(subs, many=True)
    return Response({"owner": request.user.username, "submissions": serializer.data})

@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def submit_mail_default_portfolio(request: Request, order_index: int = 1) -> Response:
    """Handles contact form submissions for the default platform portfolio."""
    owner = User.objects.filter(id=1).first() or User.objects.order_by('id').first()
    if not owner: raise Http404()
    portfolio = get_object_or_404(PortfolioSettings, owner=owner, order_index=order_index)
    return _handle_mail_submission(request, owner, portfolio)

@api_view(["POST"])
@permission_classes([AllowAny])
@throttle_classes([AnonRateThrottle])
def submit_mail_public_portfolio(request: Request, share_token: str, order_index: int = 1) -> Response:
    """Handles contact form submissions for a specific user's public portfolio."""
    owner = get_object_or_404(User, share_token=share_token, enable_share_token=True)
    portfolio = get_object_or_404(PortfolioSettings, owner=owner, order_index=order_index)
    return _handle_mail_submission(request, owner, portfolio)

def _handle_mail_submission(request: Request, owner: User, portfolio: PortfolioSettings) -> Response:
    """Internal helper to process and save validated contact form payloads."""
    print(f"Received contact form submission for {owner.email} from IP {get_request_ip(request)}")
    
    serializer = SubmissionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=owner, portfolio=portfolio, ip_address=get_request_ip(request))
    return Response({"message": "Message sent."}, status=201)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_dashboard_submission(request: Request, form_id: int) -> Response:
    """Updates a contact form submission (e.g., dismissing it or changing its priority)."""
    form = get_object_or_404(ContactFormSubmission, id=form_id, owner=request.user)
    serializer = SubmissionUpdateSerializer(form, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    form = serializer.save()
    if "display_index" in serializer.validated_data:
        form.move_to_index(serializer.validated_data["display_index"])
    return Response({"message": "Updated.", "data": SubmissionReadSerializer(form).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reorder_dashboard_submissions(request: Request) -> Response:
    """Batch reorders contact form submissions for the user's dashboard view."""
    serializer = SubmissionReorderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        reordered = ContactFormSubmission.reorder_for_owner(request.user, serializer.validated_data["order"])
        return Response({"submissions": [SubmissionReadSerializer(s).data for s in reordered]})
    except ValueError as e:
        return Response({"message": str(e)}, status=400)
    
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def trigger_user_cleanup(request: Request) -> Response:
    """Cron-triggered endpoint to securely execute the unverified user cleanup task."""
    expected_key = getattr(settings, 'CRON_SECRET_KEY', None)
    provided_key = request.headers.get("X-Cron-Secret") or request.GET.get("secret")

    if not expected_key or provided_key != expected_key:
        return Response({"message": "Unauthorized request."}, status=403)

    try:
        result = cleanup_unverified_users() 
        return Response({"message": "Cleanup task executed successfully.", "details": result}, status=200)
    except Exception as e:
        return Response({"message": f"Task failed: {str(e)}"}, status=500)

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def trigger_urgent_notifications(request: Request) -> Response:
    """Cron-triggered endpoint to securely execute the daily urgent email digests."""
    expected_key = getattr(settings, 'CRON_SECRET_KEY', None)
    provided_key = request.headers.get("X-Cron-Secret") or request.GET.get("secret")

    if not expected_key or provided_key != expected_key:
        return Response({"message": "Unauthorized request."}, status=403)

    try:
        result = process_daily_urgent_notifications() 
        return Response({"message": "Urgent notifications processed.", "details": result}, status=200)
    except Exception as e:
        return Response({"message": f"Task failed: {str(e)}"}, status=500)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def preview_all_portfolios(request: Request) -> Response:
    """Provides a lightweight list of all portfolios owned by the user for the dashboard sidebar."""
    portfolios = PortfolioSettings.objects.filter(owner=request.user).values(
        'order_index', 'name', 'title', 'is_enabled').order_by('order_index')
    portfolio_list = [
        {**p, "theme_mode": request.user.theme_mode} 
        for p in portfolios
    ]      
    return Response({
        "message": "Portfolios retrieved successfully.",
        "portfolios": portfolio_list
    }, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request: Request) -> Response:
    """Triggers a password reset OTP email for a user."""
    email = str(request.data.get("email", "")).strip().lower()
    user = User.objects.filter(email=email).first()

    if user:
        otp = ''.join(secrets.choice('0123456789') for _ in range(6))
        cache.set(f"password_reset_otp:{email}", otp, timeout=300)
        try:
            send_otp_email_task.delay(email, otp, subject="Your Password Reset OTP")
            print(f"DEBUG: Task queued for {email}")
        except Exception as e:
            print(f"CELERY ERROR: Failed to queue task for {email}. Reason: {e}")
    else:
        print(f"DEBUG: Email {email} not found in database. Skipping task.")

    return Response({"message": "If an account exists, a password reset OTP will be sent shortly."})

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request: Request) -> Response:
    """Validates the password reset OTP and applies the new password."""
    email = str(request.data.get("email", "")).strip().lower()
    otp_provided = str(request.data.get("otp", "")).strip()
    new_password = request.data.get("new_password", "")

    if cache.get(f"password_reset_otp:{email}") != otp_provided:
        return Response({"message": "Invalid or expired OTP."}, status=400)

    user = User.objects.filter(email=email).first()
    if user:
        user.set_password(new_password)
        user.save()
        cache.delete(f"password_reset_otp:{email}")
        return Response({"message": "Password reset successful."})
    
    return Response({"message": "If an account exists, the password has been reset."})