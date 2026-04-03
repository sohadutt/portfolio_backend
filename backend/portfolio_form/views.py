import re

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ContactFormSubmission, User
from .serializers import (
    ContactFormSubmissionSerializer,
    LoginSerializer,
    UserSerializer,
)


class Priority:
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3


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


def parse_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() == "true"


def parse_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


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
    serializer = ContactFormSubmissionSerializer(submission)
    data = serializer.data
    return {
        "id": data["id"],
        "display_index": data["display_index"],
        "owner": data["owner_username"],
        "owner_user_id": data["owner_user_id"],
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "message": data["message"],
        "for_work": data["for_work"],
        "priority": data["priority"],
        "is_dismissed": data["is_dismissed"],
        "submitted_at": data["submitted_at"],
    }


def build_auth_response(user):
    refresh = RefreshToken.for_user(user)
    return {
        "user_id": user.id,
        "email": user.email,
        "username": user.username,
        "share_token": user.share_token,
        "temporary_token": str(refresh),
        "bearer_token": str(refresh.access_token),
        "token_type": "Bearer",
    }


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def create_profile(request):
    email = str(request.data.get("email", "")).strip().lower()
    password = request.data.get("password", "")

    if not email or not password:
        return Response(
            {"message": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "A user with this email already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UserSerializer(
        data={
            "email": email,
            "password": password,
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
            "share_token": request.user.share_token,
        }
    )


@api_view(["POST"])
@parser_classes([JSONParser])
@permission_classes([AllowAny])
def submit_form(request, token):
    owner = get_object_or_404(User, share_token=token)
    payload = {
        "name": request.data.get("name", ""),
        "email": request.data.get("email", ""),
        "phone": request.data.get("phone"),
        "message": request.data.get("message", ""),
        "for_work": parse_bool(request.data.get("for_work")),
        "priority": parse_int(request.data.get("priority"), Priority.LOW),
        "is_dismissed": False,
    }
    serializer = ContactFormSubmissionSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    form = serializer.save(owner=owner, ip_address=get_client_ip(request))

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
    payload = {}

    if "is_dismissed" in request.data:
        payload["is_dismissed"] = parse_bool(
            request.data.get("is_dismissed"),
            default=form.is_dismissed,
        )

    if "priority" in request.data:
        payload["priority"] = parse_int(request.data.get("priority"), form.priority)

    serializer = ContactFormSubmissionSerializer(form, data=payload, partial=True)
    serializer.is_valid(raise_exception=True)
    form = serializer.save()
    new_index = request.data.get("display_index")

    if new_index is not None:
        form.move_to_index(parse_int(new_index, form.display_index))
        form.refresh_from_db()

    return Response(
        {
            "message": "Form updated successfully",
            "data": build_submission_response(form),
        },
        status=status.HTTP_200_OK,
    )
