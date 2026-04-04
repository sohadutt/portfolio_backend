from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

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


class IconAliasSerializer(serializers.Serializer):
    icon = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    iconName = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs):
        attrs["icon"] = attrs.get("icon") or attrs.get("iconName")
        return attrs


class PortfolioPersonalInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    shortName = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    github = serializers.URLField()
    linkedin = serializers.URLField()


class PortfolioHeroContentSerializer(serializers.Serializer):
    eyebrow = serializers.CharField(max_length=100)
    title = serializers.CharField()
    description = serializers.CharField()


class PortfolioAboutContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()


class PortfolioLinkSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)
    href = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
    )


class PortfolioHeroMetricSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=50)
    label = serializers.CharField(max_length=200)


class PortfolioSkillGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    items = serializers.ListField(child=serializers.CharField(), default=list)


class PortfolioProjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    eyebrow = serializers.CharField(max_length=100)
    description = serializers.CharField()
    stack = serializers.ListField(child=serializers.CharField(), default=list)
    stat = serializers.CharField(max_length=100)


class PortfolioExperienceSerializer(serializers.Serializer):
    period = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    company = serializers.CharField(max_length=200)
    relation = serializers.CharField(max_length=100)
    summary = serializers.CharField()
    highlights = serializers.ListField(child=serializers.CharField(), default=list)
    relatedComponents = serializers.ListField(
        child=serializers.CharField(),
        default=list,
    )


class PortfolioShowcaseCategorySerializer(IconAliasSerializer):
    title = serializers.CharField(max_length=200)
    relation = serializers.CharField(max_length=100)
    preview = serializers.CharField()
    items = serializers.ListField(child=serializers.CharField(), default=list)


class PortfolioFeaturedModuleSerializer(IconAliasSerializer):
    title = serializers.CharField(max_length=200)
    relation = serializers.CharField(max_length=100)
    body = serializers.CharField()
    details = serializers.CharField()


class PortfolioContactMethodSerializer(IconAliasSerializer):
    label = serializers.CharField(max_length=100)
    value = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    href = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
    )


class PortfolioStatusPillSerializer(IconAliasSerializer):
    label = serializers.CharField(max_length=100)


class PortfolioSubmissionSerializer(serializers.Serializer):
    personalInfo = PortfolioPersonalInfoSerializer()
    navigationLinks = PortfolioLinkSerializer(many=True, default=list)
    heroContent = PortfolioHeroContentSerializer()
    heroMetrics = PortfolioHeroMetricSerializer(many=True, default=list)
    aboutContent = PortfolioAboutContentSerializer()
    skillGroups = PortfolioSkillGroupSerializer(many=True, default=list)
    projects = PortfolioProjectSerializer(many=True, default=list)
    experience = PortfolioExperienceSerializer(many=True, default=list)
    showcaseCategories = PortfolioShowcaseCategorySerializer(many=True, default=list)
    featuredModules = PortfolioFeaturedModuleSerializer(many=True, default=list)
    contactMethods = PortfolioContactMethodSerializer(many=True, default=list)
    footerLinks = PortfolioLinkSerializer(many=True, default=list)
    statusPills = PortfolioStatusPillSerializer(many=True, default=list)

    def validate(self, attrs):
        owner = self.context.get("owner")
        experience = attrs.get("experience")

        if (
            owner is not None
            and experience is not None
            and not owner.su_tier
            and len(experience) > Experience.MAX_FREE_TIER_EXPERIENCES
        ):
            raise serializers.ValidationError(
                {"experience": Experience.FREE_TIER_LIMIT_MESSAGE}
            )

        return attrs

    @transaction.atomic
    def save(self, **kwargs):
        owner = kwargs.get("owner") or self.context.get("owner")
        if owner is None and self.instance is not None:
            owner = self.instance.owner

        if owner is None:
            raise ValueError("PortfolioSubmissionSerializer.save() requires an owner.")

        data = self.validated_data
        personal_info = data["personalInfo"]
        hero_content = data["heroContent"]
        about_content = data["aboutContent"]

        portfolio, _ = PortfolioSettings.objects.update_or_create(
            owner=owner,
            defaults={
                "name": personal_info["name"],
                "short_name": personal_info["shortName"],
                "title": personal_info["title"],
                "subtitle": personal_info["subtitle"],
                "location": personal_info["location"],
                "email": personal_info["email"],
                "github": personal_info["github"],
                "linkedin": personal_info["linkedin"],
                "hero_eyebrow": hero_content["eyebrow"],
                "hero_title": hero_content["title"],
                "hero_description": hero_content["description"],
                "about_title": about_content["title"],
                "about_description": about_content["description"],
            },
        )

        self._replace_ordered_records(
            HeroMetric,
            owner,
            [
                {"value": item["value"], "label": item["label"]}
                for item in data["heroMetrics"]
            ],
        )
        self._replace_ordered_records(
            SkillGroup,
            owner,
            [
                {
                    "title": item["title"],
                    "description": item["description"],
                    "items": item["items"],
                }
                for item in data["skillGroups"]
            ],
        )
        self._replace_ordered_records(
            Project,
            owner,
            [
                {
                    "title": item["title"],
                    "eyebrow": item["eyebrow"],
                    "description": item["description"],
                    "stack": item["stack"],
                    "stat": item["stat"],
                }
                for item in data["projects"]
            ],
        )
        self._replace_ordered_records(
            Experience,
            owner,
            [
                {
                    "period": item["period"],
                    "title": item["title"],
                    "company": item["company"],
                    "relation": item["relation"],
                    "summary": item["summary"],
                    "highlights": item["highlights"],
                    "related_components": item["relatedComponents"],
                }
                for item in data["experience"]
            ],
        )
        self._replace_ordered_records(
            ShowcaseCategory,
            owner,
            [
                {
                    "title": item["title"],
                    "icon_name": item["icon"],
                    "relation": item["relation"],
                    "preview": item["preview"],
                    "items": item["items"],
                }
                for item in data["showcaseCategories"]
            ],
        )
        self._replace_ordered_records(
            FeaturedModule,
            owner,
            [
                {
                    "title": item["title"],
                    "icon_name": item["icon"],
                    "relation": item["relation"],
                    "body": item["body"],
                    "details": item["details"],
                }
                for item in data["featuredModules"]
            ],
        )

        Link.objects.filter(owner=owner).delete()
        self._create_links(owner, Link.LinkType.NAV, data["navigationLinks"])
        self._create_links(owner, Link.LinkType.CONTACT, data["contactMethods"])
        self._create_links(owner, Link.LinkType.FOOTER, data["footerLinks"])
        self._create_links(owner, Link.LinkType.STATUS, data["statusPills"])

        return portfolio

    def _replace_ordered_records(self, model, owner, items):
        model.objects.filter(owner=owner).delete()
        objects = [
            model(owner=owner, order=index, **item)
            for index, item in enumerate(items, start=1)
        ]
        if objects:
            model.objects.bulk_create(objects)

    def _create_links(self, owner, link_type, items):
        Link.objects.bulk_create(
            [
                Link(
                    owner=owner,
                    order=index,
                    type=link_type,
                    label=item["label"],
                    value=item.get("value"),
                    href=item.get("href"),
                    icon_name=item.get("icon"),
                )
                for index, item in enumerate(items, start=1)
            ]
        )
