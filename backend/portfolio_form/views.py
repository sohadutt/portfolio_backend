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

from .models import ContactFormSubmission, PortfolioSettings, User
from .serializers import (
    LoginSerializer,
    ProfileCreateSerializer,
    SubmissionCreateSerializer,
    SubmissionReadSerializer,
    SubmissionReorderSerializer,
    SubmissionUpdateSerializer,
)


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    return Response({"detail": "CSRF cookie set"})


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def build_username_from_email(email):
    base_username = email.split("@")[0].strip().lower()
    base_username = re.sub(r"[^a-z0-9._+-]", "", base_username) or "user"
    username = base_username
    suffix = 1

    while User.objects.filter(username=username).exists():
        username = f"{base_username}{suffix}"
        suffix += 1

    return username


def build_submission_response(submission):
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


def build_auth_response(user):
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


def resolve_submission_target(token):
    owner = User.objects.filter(share_token=token, enable_share_token=True).first()
    if owner is None:
        raise Http404("Share link not found.")

    portfolio = PortfolioSettings.objects.filter(owner=owner).first()
    return owner, portfolio


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def create_profile(request):
    email = str(request.data.get("email", "")).strip().lower()
    serializer = ProfileCreateSerializer(
        data={
            "email": email,
            "password": request.data.get("password", ""),
            "username": build_username_from_email(email),
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
def login(request):
    serializer = LoginSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    return Response(
        {
            "message": "Login successful",
            "data": build_auth_response(user),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_tokens(request):
    return Response(
        {
            "enable_share_token": request.user.enable_share_token,
            "share_token": request.user.share_token,
        }
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def submit_form(request, token):
    owner, portfolio = resolve_submission_target(token)
    serializer = SubmissionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    form = serializer.save(
        owner=owner,
        portfolio=portfolio,
        ip_address=get_client_ip(request),
        is_dismissed=False,
    )

    return Response(
        {
            "message": "Form submitted successfully",
            "data": build_submission_response(form),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_submissions(request):
    submissions = ContactFormSubmission.objects.filter(owner=request.user)

    return Response(
        {
            "owner": request.user.username,
            "owner_user_id": request.user.id,
            "submissions": [
                build_submission_response(submission) for submission in submissions
            ],
        }
    )


@api_view(["PATCH", "POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def update_submission(request, form_id):
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
            "data": build_submission_response(form),
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def reorder_submissions(request):
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
            "submissions": [
                build_submission_response(submission) for submission in reordered
            ],
        },
        status=status.HTTP_200_OK,
    )
