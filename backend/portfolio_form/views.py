import re

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


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
        "share_token": user.share_token,
        "temporary_token": str(refresh),
        "bearer_token": str(refresh.access_token),
        "token_type": "Bearer",
    }


def resolve_share_submission_target(share_token):
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
            enable_share_token=True,).first()
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


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def create_user_profile(request):
    email = str(request.data.get("email", "")).strip().lower()
    serializer = ProfileCreateSerializer(
        data={
            "email": email,
            "password": request.data.get("password", ""),
            "username": generate_username_from_email(email),
        }
    )
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response(
        {
            "message": "Profile created successfully",
            "data": {
                "user_id": user.id,
                "email": user.email,
                "username": user.username,
                "enable_share_token": user.enable_share_token,
                "share_token": user.share_token,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

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
    serializer = SubmissionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    form = serializer.save(
        owner=owner,
        portfolio=portfolio,
        ip_address=get_request_ip(request),
        is_dismissed=False,
    )

    return Response(
        {
            "message": "Form submitted successfully",
            "data": serialize_submission(form),
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def submit_mail_public_portfolio(request, share_token):
    owner, portfolio = resolve_share_submission_target(share_token)
    serializer = SubmissionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    form = serializer.save(
        owner=owner,
        portfolio=portfolio,
        ip_address=get_request_ip(request),
        is_dismissed=False,
    )

    return Response(
        {
            "message": "Form submitted successfully",
            "data": serialize_submission(form),
        },
        status=status.HTTP_201_CREATED,
    )


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
    owner = resolve_public_portfolio_owner()
    return Response(serialize_public_portfolio(owner))


@api_view(["GET"])
@permission_classes([AllowAny])
def get_shared_public_portfolio(request, share_token):
    owner = resolve_public_portfolio_owner(share_token)
    return Response(serialize_public_portfolio(owner))


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def submit_portfolio(request):
    serializer = PortfolioSubmissionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(owner=request.user)
    return Response(
        {"message": "Portfolio saved successfully", "data": serialize_public_portfolio(request.user)},
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def update_portfolio(request):
    portfolio = PortfolioSettings.objects.filter(owner=request.user).first()
    if not portfolio:
        return Response(
            {"message": "Portfolio not found for user."},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = PortfolioSubmissionSerializer(portfolio, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        {"message": "Portfolio updated successfully", "data": serialize_public_portfolio(request.user)},
        status=status.HTTP_200_OK,
    )