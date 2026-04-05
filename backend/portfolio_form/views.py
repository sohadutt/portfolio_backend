import re
import time
import secrets
import random
import vercel_blob

from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from .utils import compress_to_webp
from .tasks import send_otp_email_task
from .models import (
    ContactFormSubmission, Experience, FeaturedModule, HeroMetric, 
    Link, PortfolioSettings, Project, ShowcaseCategory, SkillGroup, User
)
from .serializers import (
    LoginSerializer, PortfolioSubmissionSerializer, ProfileCreateSerializer,
    SubmissionCreateSerializer, SubmissionReadSerializer, SubmissionReorderSerializer,
    SubmissionUpdateSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({"detail": "CSRF cookie set"})

def get_request_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR")

def _check_rate_limit(request):
    client_ip = get_request_ip(request) or "unknown"
    blocked_key = f"contact_form_blocked:{client_ip}"
    attempts_key = f"contact_form_attempts:{client_ip}"

    if cache.get(blocked_key):
        return Response({"message": "Too many requests. Try again later."}, status=429)

    now = int(time.time())
    window = settings.CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS
    recent_attempts = [t for t in cache.get(attempts_key, []) if t > now - window]

    if len(recent_attempts) >= settings.CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS:
        cache.set(blocked_key, True, timeout=settings.CONTACT_FORM_BLOCK_SECONDS)
        return Response({"message": "Access temporarily blocked."}, status=429)

    recent_attempts.append(now)
    cache.set(attempts_key, recent_attempts, timeout=window)
    return None

def generate_username_from_email(email):
    base = re.sub(r"[^a-z0-9._+-]", "", email.split("@")[0].lower()) or "user"
    username, suffix = base, 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{suffix}"
        suffix += 1
    return username

@api_view(["POST"])
@permission_classes([AllowAny])
def create_user_profile(request):
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
def auth_otp(request):
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
def verify_otp(request):
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
def login_user(request):
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    u = request.user
    return Response({
        "user_id": u.id, "email": u.email, "username": u.username,
        "first_name": u.first_name, "last_name": u.last_name,
        "profile_picture": u.profile_picture_url,
        "theme_mode": u.theme_mode,
        "tier": u.tier,
        "is_verified": u.is_verified, "enable_share_token": u.enable_share_token,
        "share_token": u.share_token if (u.is_verified and u.enable_share_token) else None
    })

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def update_user_profile(request):
    user = request.user
    
    # Update names
    user.first_name = request.data.get("first_name", user.first_name)
    user.last_name = request.data.get("last_name", user.last_name)

    # Update theme
    if "theme_mode" in request.data:
        try:
            user.theme_mode = int(request.data.get("theme_mode"))
        except (ValueError, TypeError):
            return Response({"error": "theme_mode must be an integer."}, status=400)

    # Process Image
    if "profile_picture" in request.FILES:
        old_url = user.profile_picture_url
        original_file = request.FILES["profile_picture"]
        
        try:
            webp_file = compress_to_webp(original_file)
            webp_file.seek(0)
            
            random_suffix = secrets.token_hex(3)
            filename = f"u{user.id}_{random_suffix}.webp"
            
            resp = vercel_blob.put(
                path=f"profile_pics/{filename}", 
                data=webp_file.read(), 
                options={
                    "access": "public", # THIS WILL NOW WORK ON YOUR PUBLIC STORE
                    "content_type": "image/webp"
                }
            )
            
            user.profile_picture_url = resp["url"]

            # Clean up old blob if it exists
            if old_url and "vercel-storage.com" in old_url:
                try:
                    vercel_blob.delete(old_url)
                except Exception:
                    pass 

        except Exception as e:
            return Response({"error": f"Upload failed: {str(e)}"}, status=500)
    print(f"DEBUG: Updated profile picture URL: {user.profile_picture_url}")
    user.save()

    # Cast the URL to string to ensure it's JSON serializable
    return Response({
        "message": "Profile updated successfully.", 
        "data": {
            "first_name": user.first_name, 
            "last_name": user.last_name, 
            "theme_mode": user.theme_mode,
            "profile_picture": str(user.profile_picture_url) if user.profile_picture_url else None,
        }
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def status_share_token(request):
    user = request.user
    if not user.is_verified:
        return Response({"message": "Verify email to enable sharing."}, status=403)

    user.enable_share_token = not user.enable_share_token
    user.save()
    return Response({
        "enable_share_token": user.enable_share_token,
        "share_token": user.share_token if user.enable_share_token else None
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_tokens(request):
    return Response({
        "enable_share_token": request.user.enable_share_token,
        "share_token": request.user.share_token,
    })

def serialize_portfolio_data(owner, request=None):
    profile = get_object_or_404(PortfolioSettings, owner=owner)

    def paginate_qs(queryset):
        if request:
            paginator = StandardResultsSetPagination()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                return paginator.get_paginated_response(list(page)).data
        return list(queryset)

    return {
        "themeMode": owner.theme_mode,
        "personalInfo": {
            "name": profile.name, "shortName": profile.short_name, "title": profile.title, 
            "subtitle": profile.subtitle, "location": profile.location, "email": profile.email, 
            "github": profile.github, "linkedin": profile.linkedin, "profilePicture": owner.profile_picture_url
        },
        "heroContent": {"eyebrow": profile.hero_eyebrow, "title": profile.hero_title, "description": profile.hero_description},
        "heroMetrics": list(HeroMetric.objects.filter(owner=owner).values("value", "label")),
        "aboutContent": {"title": profile.about_title, "description": profile.about_description},
        "skillGroups": list(SkillGroup.objects.filter(owner=owner).values("title", "description", "items")),
        "projects": paginate_qs(Project.objects.filter(owner=owner).values("title", "eyebrow", "description", "stack", "stat")),
        "experience": paginate_qs(Experience.objects.filter(owner=owner).values("period", "title", "company", "relation", "summary", "highlights")),
        "showcaseCategories": list(ShowcaseCategory.objects.filter(owner=owner).values("title", "icon_name", "relation", "preview", "items")),
        "featuredModules": list(FeaturedModule.objects.filter(owner=owner).values("title", "icon_name", "relation", "body", "details")),
        "contactMethods": list(Link.objects.filter(owner=owner, type="CONTACT").values("label", "value", "href", "icon_name")),
        "navigationLinks": list(Link.objects.filter(owner=owner, type="NAV").values("label", "href")),
        "footerLinks": list(Link.objects.filter(owner=owner, type="FOOTER").values("label", "href")),
        "statusPills": list(Link.objects.filter(owner=owner, type="STATUS").values("label", "icon_name")),
    }

@api_view(["GET"])
@permission_classes([AllowAny])
def get_default_public_portfolio(request):
    owner = User.objects.filter(id=1).first() or User.objects.order_by('id').first()
    if not owner: raise Http404()
    return Response(serialize_portfolio_data(owner, request))

@api_view(["GET"])
@permission_classes([AllowAny])
def get_shared_public_portfolio(request, share_token):
    owner = get_object_or_404(User, share_token=share_token, enable_share_token=True)
    return Response(serialize_portfolio_data(owner, request))

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_portfolio(request):
    if not request.user.is_verified:
        return Response({"message": "Verify first."}, status=403)
    serializer = PortfolioSubmissionSerializer(data=request.data, context={"owner": request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=request.user)
    return Response({"message": "Portfolio saved.", "data": serialize_portfolio_data(request.user)})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_portfolio(request):
    return submit_portfolio(request)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_dashboard_submissions(request):
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
def submit_mail_default_portfolio(request):
    owner = User.objects.filter(id=1).first() or User.objects.order_by('id').first()
    if not owner: raise Http404()
    portfolio = PortfolioSettings.objects.filter(owner=owner).first()
    return _handle_mail_submission(request, owner, portfolio)

@api_view(["POST"])
@permission_classes([AllowAny])
def submit_mail_public_portfolio(request, share_token):
    owner = get_object_or_404(User, share_token=share_token, enable_share_token=True)
    portfolio = PortfolioSettings.objects.filter(owner=owner).first()
    return _handle_mail_submission(request, owner, portfolio)

def _handle_mail_submission(request, owner, portfolio):
    limit_check = _check_rate_limit(request)
    if limit_check: return limit_check
    serializer = SubmissionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=owner, portfolio=portfolio, ip_address=get_request_ip(request))
    return Response({"message": "Message sent."}, status=201)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_dashboard_submission(request, form_id):
    form = get_object_or_404(ContactFormSubmission, id=form_id, owner=request.user)
    serializer = SubmissionUpdateSerializer(form, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    form = serializer.save()
    if "display_index" in serializer.validated_data:
        form.move_to_index(serializer.validated_data["display_index"])
    return Response({"message": "Updated.", "data": SubmissionReadSerializer(form).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reorder_dashboard_submissions(request):
    serializer = SubmissionReorderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        reordered = ContactFormSubmission.reorder_for_owner(request.user, serializer.validated_data["order"])
        return Response({"submissions": [SubmissionReadSerializer(s).data for s in reordered]})
    except ValueError as e:
        return Response({"message": str(e)}, status=400)