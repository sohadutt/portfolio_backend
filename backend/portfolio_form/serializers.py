from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import ContactFormSubmission, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "share_token", "dashboard_token", "created_at"]
        read_only_fields = ["id", "share_token", "dashboard_token", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class ContactFormSubmissionSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_user_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = ContactFormSubmission
        fields = [
            "id",
            "owner",
            "owner_username",
            "owner_user_id",
            "name",
            "email",
            "phone",
            "message",
            "for_work",
            "submitted_at",
            "ip_address",
            "priority",
            "is_dismissed",
            "display_index",
        ]
        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "owner_user_id",
            "submitted_at",
            "ip_address",
            "display_index",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

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
