from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import ContactFormSubmission, User


class ProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "enable_share_token",
            "share_token",
            "created_at",
        ]
        read_only_fields = ["id", "share_token", "created_at"]

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class SubmissionReadSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_user_id = serializers.IntegerField(source="owner.id", read_only=True)
    portfolio_id = serializers.IntegerField(source="portfolio.id", read_only=True)
    priority_label = serializers.CharField(source="get_priority_display", read_only=True)

    class Meta:
        model = ContactFormSubmission
        fields = [
            "id",
            "display_index",
            "owner_username",
            "owner_user_id",
            "portfolio_id",
            "name",
            "email",
            "phone",
            "message",
            "for_work",
            "priority",
            "priority_label",
            "is_dismissed",
            "submitted_at",
        ]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ["name", "email", "phone", "message", "for_work", "priority"]

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_message(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message is required.")
        return value

    def validate_phone(self, value):
        if value in (None, ""):
            return None
        return value.strip()


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    display_index = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = ContactFormSubmission
        fields = ["is_dismissed", "priority", "display_index"]


class SubmissionReorderSerializer(serializers.Serializer):
    order = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]
        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        authenticated_user = authenticate(
            request=self.context.get("request"),
            username=user.username,
            password=password,
        )

        if authenticated_user is None:
            raise serializers.ValidationError("Invalid email or password")

        attrs["user"] = authenticated_user
        attrs["email"] = email
        return attrs
