import re
import time
import secrets
import random

from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_otp_email_task

from .models import (
    ContactFormSubmission,
    Experience,
    FeaturedModule,
    HeroMetric,
    Link,
    PortfolioSettings,
    Project,
    ShowcaseCategory,
    SkillGroup,
    User,
)
from .serializers import (
    LoginSerializer,
    PortfolioSubmissionSerializer,
    ProfileCreateSerializer,
    SubmissionCreateSerializer,
    SubmissionReadSerializer,
    SubmissionReorderSerializer,
    SubmissionUpdateSerializer,
)


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return Response({"detail": "CSRF cookie set"})


def get_request_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _submission_rate_limit_response(request):
    client_ip = get_request_ip(request) or "unknown"
    blocked_key = f"contact_form_blocked:{client_ip}"
    attempts_key = f"contact_form_attempts:{client_ip}"

    if cache.get(blocked_key):
        return Response(
            {
                "message": "Too many requests from this client. Try again later.",
                "blocked_for_seconds": settings.CONTACT_FORM_BLOCK_SECONDS,
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    now = int(time.time())
    window_start = now - settings.CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS
    recent_attempts = [
        attempt
        for attempt in cache.get(attempts_key, [])
        if attempt > window_start
    ]

    if len(recent_attempts) >= settings.CONTACT_FORM_RATE_LIMIT_MAX_REQUESTS:
        cache.set(blocked_key, True, timeout=settings.CONTACT_FORM_BLOCK_SECONDS)
        cache.delete(attempts_key)
        return Response(
            {
                "message": "Too many requests from this client. Access temporarily blocked.",
                "blocked_for_seconds": settings.CONTACT_FORM_BLOCK_SECONDS,
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    recent_attempts.append(now)
    cache.set(
        attempts_key,
        recent_attempts,
        timeout=settings.CONTACT_FORM_RATE_LIMIT_WINDOW_SECONDS,
    )
    return None


def generate_username_from_email(email):
    base_username = email.split("@")[0].strip().lower()
    base_username = re.sub(r"[^a-z0-9._+-]", "", base_username) or "user"
    username = base_username
    suffix = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{suffix}"
        suffix += 1

    return username


def serialize_submission(submission):
    serializer = SubmissionReadSerializer(submission)
    data = serializer.data
    return {
        "id": data["id"],
        "display_index": data["display_index"],
        "owner": data["owner_username"],
        "owner_user_id": data["owner_user_id"],
        "portfolio_id": data.get("portfolio_id"),
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "message": data["message"],
        "for_work": data["for_work"],
        "priority": data["priority"],
        "priority_label": data["priority_label"],
        "is_dismissed": data["is_dismissed"],
        "submitted_at": data["submitted_at"],
    }


def build_login_response(user):
    refresh = RefreshToken.for_user(user)
    return {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "enable_share_token": user.enable_share_token,
        "is_verified": user.is_verified,
        "share_token": user.share_token,
        "temporary_token": str(refresh),
        "bearer_token": str(refresh.access_token),
        "token_type": "Bearer",
    }


def get_owner_from_share_token(share_token):
    owner = User.objects.filter(
        share_token=share_token,
        enable_share_token=True,
    ).first()
    if owner is None:
        raise Http404("Share link not found.")

    portfolio = PortfolioSettings.objects.filter(owner=owner).first()
    return owner, portfolio


def get_default_public_owner():
    owner = User.objects.filter(id=1).first()
    if owner is None:
        owner = User.objects.order_by("id").first()
    if owner is None:
        raise Http404("Default portfolio not found.")
    return owner


def resolve_public_portfolio_owner(share_token=None):
    if share_token:
        owner = User.objects.filter(
            share_token=share_token,
            enable_share_token=True,
        ).first()
        if owner is None:
            raise Http404("Share link not found.")
        return owner

    return get_default_public_owner()


def serialize_public_portfolio(owner):
    portfolio = get_object_or_404(PortfolioSettings, owner=owner)

    navigation_links = list(
        Link.objects.filter(owner=owner, type=Link.LinkType.NAV).values("label", "href")
    )
    footer_links = list(
        Link.objects.filter(owner=owner, type=Link.LinkType.FOOTER).values("label", "href")
    )
    contact_methods = list(
        Link.objects.filter(owner=owner, type=Link.LinkType.CONTACT).values(
            "label",
            "value",
            "href",
            "icon_name",
        )
    )
    status_pills = list(
        Link.objects.filter(owner=owner, type=Link.LinkType.STATUS).values(
            "label",
            "icon_name",
        )
    )

    return {
        "personalInfo": {
            "name": portfolio.name,
            "shortName": portfolio.short_name,
            "title": portfolio.title,
            "subtitle": portfolio.subtitle,
            "location": portfolio.location,
            "email": portfolio.email,
            "github": portfolio.github,
            "linkedin": portfolio.linkedin,
        },
        "navigationLinks": navigation_links,
        "heroContent": {
            "eyebrow": portfolio.hero_eyebrow,
            "title": portfolio.hero_title,
            "description": portfolio.hero_description,
        },
        "heroMetrics": list(
            HeroMetric.objects.filter(owner=owner).values("value", "label")
        ),
        "aboutContent": {
            "title": portfolio.about_title,
            "description": portfolio.about_description,
        },
        "skillGroups": list(
            SkillGroup.objects.filter(owner=owner).values(
                "title",
                "description",
                "items",
            )
        ),
        "projects": list(
            Project.objects.filter(owner=owner).values(
                "title",
                "eyebrow",
                "description",
                "stack",
                "stat",
            )
        ),
        "experience": [
            {
                "period": item.period,
                "title": item.title,
                "company": item.company,
                "relation": item.relation,
                "summary": item.summary,
                "highlights": item.highlights,
                "relatedComponents": item.related_components,
            }
            for item in Experience.objects.filter(owner=owner)
        ],
        "showcaseCategories": [
            {
                "title": item.title,
                "icon": item.icon_name,
                "relation": item.relation,
                "preview": item.preview,
                "items": item.items,
            }
            for item in ShowcaseCategory.objects.filter(owner=owner)
        ],
        "featuredModules": [
            {
                "title": item.title,
                "icon": item.icon_name,
                "relation": item.relation,
                "body": item.body,
                "details": item.details,
            }
            for item in FeaturedModule.objects.filter(owner=owner)
        ],
        "contactMethods": [
            {
                "label": item["label"],
                "value": item["value"],
                "href": item["href"],
                "icon": item["icon_name"],
            }
            for item in contact_methods
        ],
        "footerLinks": footer_links,
        "statusPills": [
            {
                "label": item["label"],
                "icon": item["icon_name"],
            }
            for item in status_pills
        ],
    }


def enquiry_submission_for_owner(request, owner, portfolio):
    rate_limit_response = _submission_rate_limit_response(request)
    if rate_limit_response is not None:
        return rate_limit_response

    serializer = SubmissionCreateSerializer(
        data=request.data,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(
        owner=owner,
        portfolio=portfolio,
        ip_address=get_request_ip(request),
        is_dismissed=False,
    )
    return Response(
        {
            "message": "Form submitted successfully",
            "data": serialize_submission(serializer.instance),
        },
        status=status.HTTP_201_CREATED,
    )


def public_portfolio_response(share_token=None):
    owner = resolve_public_portfolio_owner(share_token)
    return Response(serialize_public_portfolio(owner))


def save_portfolio_for_user(request, *, partial):
    if not request.user.is_verified:
        return Response(
            {
                "message": "Email verification required to save portfolio. Please check your email for the OTP code and verify your account.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    serializer_kwargs = {
        "data": request.data,
        "context": {"owner": request.user},
        "partial": partial,
    }
    success_message = "Portfolio updated successfully"
    if partial:
        portfolio = PortfolioSettings.objects.filter(owner=request.user).first()
        if not portfolio:
            return Response(
                {"message": "Portfolio not found for user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PortfolioSubmissionSerializer(portfolio, **serializer_kwargs)
        success_status = status.HTTP_200_OK
    else:
        serializer = PortfolioSubmissionSerializer(**serializer_kwargs)
        success_message = "Portfolio saved successfully"
        success_status = status.HTTP_201_CREATED

    serializer.is_valid(raise_exception=True)
    serializer.save(owner=request.user)
    return Response(
        {
            "message": success_message,
            "data": serialize_public_portfolio(request.user),
        },
        status=success_status,
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def create_user_profile(request):
    """
    Creates a new user profile and immediately triggers an OTP 
    verification email via Celery.
    """
    email = str(request.data.get("email", "")).strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response(
            {"message": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 1. Validate and Create User
    # We use the serializer to handle password hashing and unique email checks
    serializer = ProfileCreateSerializer(
        data={
            "email": email,
            "password": password,
            "username": generate_username_from_email(email),
        }
    )
    
    if not serializer.is_valid():
        return Response(
            {"message": "Registration failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = serializer.save()

    # 2. Generate and Cache OTP for immediate verification
    # This prevents the user from having to 'request' an OTP after signing up
    secure_otp = ''.join(secrets.choice('0123456789') for i in range(6))
    
    # Store in cache (Redis) for 3 minutes
    cache.set(f"otp:{email}", secure_otp, timeout=200)

    # 3. Trigger Celery Task
    try:
        send_otp_email_task.delay(email, secure_otp)
        otp_status = "OTP sent to your email."
    except Exception:
        # If Redis/Celery is down, the user is still created, 
        # but they'll need to request a new OTP later via auth_otp.
        otp_status = "Profile created, but we couldn't send the verification email. Please try logging in to resend."

    return Response(
        {
            "message": f"Profile created successfully. {otp_status}",
            "data": {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "is_verified": user.is_verified, # Will be False initially
            },
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def auth_otp(request):
    email = str(request.data.get("email", "")).strip().lower()
    
    if not email:
        return Response(
            {"message": "Email is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 1. Silent Check: Look for the user
    user = User.objects.filter(email=email).first()

    # 2. Ambiguous Flow: 
    if not user:
        time.sleep(random.uniform(0.1, 0.3))
    # If the user exists, we do the work. If not, we do NOTHING.
    if user:
        secure_otp = ''.join(secrets.choice('0123456789') for i in range(6))
        cache.set(f"otp:{email}", secure_otp, timeout=200)
        
        try:
            send_otp_email_task.delay(email, secure_otp)
        except Exception:
            # Log this internally, but don't tell the user why it failed
            pass 

    # 3. Identical Response: 
    # Whether the user existed or not, the attacker sees the SAME message.
    return Response(
        {"message": "If an account is associated with this email, you will receive an OTP shortly."},
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def verify_otp(request):
    email = str(request.data.get("email", "")).strip().lower()
    otp_provided = str(request.data.get("otp", "")).strip()

    if not email or not otp_provided:
        return Response(
            {"message": "Email and OTP are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 1. Check if the OTP exists in the cache and matches
    cached_otp = cache.get(f"otp:{email}")
    
    if cached_otp is None or cached_otp != otp_provided:
        return Response(
            {"message": "Invalid or expired OTP."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 2. Fetch the user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # 3. Verify the user (Complete the partial profile)
    if not user.is_verified:
        user.is_verified = True
        user.save()

    # 4. Clear the OTP from the cache so it can't be reused
    cache.delete(f"otp:{email}")

    # 5. Generate JWT tokens for login
    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "OTP verified successfully.",
            "data": {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "is_verified": user.is_verified,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    is_verified = user.is_verified
    if not is_verified:
        return Response(
            {
                "message": "Email verification required. Please check your email for the OTP code and verify your account.",
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    return Response(
        {
            "message": "Login successful",
            "data": build_login_response(user),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile_tokens(request):
    return Response(
        {
            "enable_share_token": request.user.enable_share_token,
            "share_token": request.user.share_token,
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def submit_mail_default_portfolio(request):
    owner = resolve_public_portfolio_owner()
    portfolio = PortfolioSettings.objects.filter(owner=owner).first()
    return enquiry_submission_for_owner(request, owner, portfolio)


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def submit_mail_public_portfolio(request, share_token):
    owner, portfolio = get_owner_from_share_token(share_token)
    return enquiry_submission_for_owner(request, owner, portfolio)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_dashboard_submissions(request):
    submissions = ContactFormSubmission.objects.filter(owner=request.user)

    return Response(
        {
            "owner": request.user.username,
            "owner_user_id": request.user.id,
            "submissions": [serialize_submission(submission) for submission in submissions],
        }
    )


@api_view(["PATCH", "POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def update_dashboard_submission(request, form_id):
    form = get_object_or_404(ContactFormSubmission, id=form_id, owner=request.user)
    serializer = SubmissionUpdateSerializer(form, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    form = serializer.save()
    new_index = serializer.validated_data.get("display_index")

    if new_index is not None:
        form.move_to_index(new_index)
        form.refresh_from_db()

    return Response(
        {
            "message": "Form updated successfully",
            "data": serialize_submission(form),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def reorder_dashboard_submissions(request):
    serializer = SubmissionReorderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        reordered = ContactFormSubmission.reorder_for_owner(
            request.user,
            serializer.validated_data["order"],
        )
    except ValueError as exc:
        return Response(
            {"message": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "Submissions reordered successfully",
            "submissions": [serialize_submission(submission) for submission in reordered],
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def get_default_public_portfolio(request):
    return public_portfolio_response()


@api_view(["GET"])
@permission_classes([AllowAny])
def get_shared_public_portfolio(request, share_token):
    return public_portfolio_response(share_token)


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def submit_portfolio(request):
    return save_portfolio_for_user(request, partial=False)


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def update_portfolio(request):
    return save_portfolio_for_user(request, partial=True)

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def status_share_token(request):
    """
    Toggles the share token on/off. 
    Strictly requires the user to be verified first.
    """
    user = request.user
    
    # 1. Block unverified users from enabling sharing
    if not user.is_verified:
        return Response(
            {"message": "Please verify your email address to enable portfolio sharing."},
            status=status.HTTP_403_FORBIDDEN
        )

    # 2. Toggle the boolean
    user.enable_share_token = not user.enable_share_token
    user.save()
    
    status_label = "enabled" if user.enable_share_token else "disabled"
    
    return Response(
        {
            "message": f"Portfolio sharing is now {status_label}.",
            "enable_share_token": user.enable_share_token,
            "share_token": user.share_token if user.enable_share_token else None
        },
        status=status.HTTP_200_OK
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Retrieves the logged-in user's profile details.
    Hides the share_token string if the user is unverified or sharing is disabled.
    """
    user = request.user
    
    # Base data structure
    profile_data = {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "is_verified": user.is_verified,
        "enable_share_token": user.enable_share_token,
    }

    # Only provide the actual token if the gatekeeping requirements are met
    if user.is_verified and user.enable_share_token:
        profile_data["share_token"] = user.share_token
    else:
        profile_data["share_token"] = None

    return Response(profile_data, status=status.HTTP_200_OK)