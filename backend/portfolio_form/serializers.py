from __future__ import annotations

from typing import Any

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from .models import (
    ContactFormSubmission, Experience, FeaturedModule, HeroMetric,
    Link, PortfolioSettings, Project, ShowcaseCategory, SkillGroup, User,
)

PortfolioPayload = dict[str, Any]

class ProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "first_name", 
            "last_name", "enable_share_token", "is_verified", 
            "share_token", "created_at",
        ]
        read_only_fields = ["id", "share_token", "created_at", "is_verified"]

    def validate_email(self, value: str) -> str:
        email = value.strip().lower()
        if User.objects.filter(email=email, is_verified=True).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> User:
        email = validated_data.get("email")
        password = validated_data.pop("password")
        
        user = User.objects.filter(email=email).first()
        
        if user:
            for attr, value in validated_data.items():
                setattr(user, attr, value)
            user.set_password(password)
            user.is_verified = False 
            user.save()
        else:
            user = User(**validated_data)
            user.set_password(password)
            user.is_verified = False # Users should start unverified until OTP is confirmed
            user.save()
            
        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture", "theme_mode"]

    def validate_profile_picture(self, value: Any) -> Any:
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be under 2MB.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture_url"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        email = attrs["email"].strip().lower()
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        authenticated_user = authenticate(
            request=self.context.get("request"),
            username=user.username,
            password=attrs["password"],
        )

        if not authenticated_user:
            raise serializers.ValidationError("Invalid email or password")

        attrs["user"] = authenticated_user
        attrs["email"] = email
        return attrs

class IconAliasSerializer(serializers.Serializer):
    icon = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    iconName = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        attrs["icon"] = attrs.get("icon") or attrs.get("iconName")
        return attrs


def deep_merge_portfolio_data(current: Any, incoming: Any) -> Any:
    if isinstance(current, dict) and isinstance(incoming, dict):
        merged = dict(current)
        for key, value in incoming.items():
            merged[key] = deep_merge_portfolio_data(merged.get(key), value)
        return merged
    return incoming


def set_serializer_partial(field: Any, is_partial: bool) -> None:
    if not isinstance(field, serializers.BaseSerializer):
        return
    field.partial = is_partial
    child = getattr(field, "child", None)
    if isinstance(child, serializers.BaseSerializer):
        set_serializer_partial(child, is_partial)
    nested_fields = getattr(field, "fields", None)
    if nested_fields:
        for nested in nested_fields.values():
            set_serializer_partial(nested, is_partial)


def serialize_portfolio_payload(portfolio: PortfolioSettings) -> PortfolioPayload:
    all_links = list(
        Link.objects.filter(portfolio=portfolio)
        .order_by("order", "id")
        .values("type", "label", "value", "href", "icon_name")
    )

    return {
        "new_order_index": portfolio.order_index,
        "is_enabled": portfolio.is_enabled,
        "personalInfo": {
            "name": portfolio.name,
            "shortName": portfolio.short_name,
            "title": portfolio.title,
            "subtitle": portfolio.subtitle,
            "location": portfolio.location,
            "email": portfolio.email,
            "github": portfolio.github,
            "linkedin": portfolio.linkedin,
            "profilePicture": portfolio.owner.profile_picture_url,
        },
        "navigationLinks": [
            {"label": link["label"], "href": link["href"]}
            for link in all_links
            if link["type"] == Link.LinkType.NAV
        ],
        "heroContent": {
            "eyebrow": portfolio.hero_eyebrow,
            "title": portfolio.hero_title,
            "description": portfolio.hero_description,
        },
        "heroActions": portfolio.hero_actions or {},
        "heroMetrics": list(
            HeroMetric.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values("value", "label")
        ),
        "heroFocus": portfolio.hero_focus or {},
        "heroBadges": portfolio.hero_badges or [],
        "heroHighlights": portfolio.hero_highlights or [],
        "aboutContent": {
            "title": portfolio.about_title,
            "description": portfolio.about_description,
        },
        "skillGroups": list(
            SkillGroup.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values("title", "description", "items")
        ),
        "projects": [
            {
                "title": item["title"],
                "eyebrow": item["eyebrow"],
                "description": item["description"],
                "stack": item["stack"],
                "stat": item["stat"],
                "href": item["href"],
                "ctaLabel": item["cta_label"],
                "icon": item["icon_name"],
            }
            for item in Project.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values("title", "eyebrow", "description", "stack", "stat", "href", "cta_label", "icon_name")
        ],
        "experience": [
            {
                "period": item["period"],
                "title": item["title"],
                "company": item["company"],
                "relation": item["relation"],
                "summary": item["summary"],
                "highlights": item["highlights"],
                "relatedComponents": item["related_components"],
            }
            for item in Experience.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values(
                "period",
                "title",
                "company",
                "relation",
                "summary",
                "highlights",
                "related_components",
            )
        ],
        "showcaseCategories": [
            {
                "title": item["title"],
                "icon": item["icon_name"],
                "relation": item["relation"],
                "preview": item["preview"],
                "items": item["items"],
            }
            for item in ShowcaseCategory.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values("title", "icon_name", "relation", "preview", "items")
        ],
        "featuredModules": [
            {
                "title": item["title"],
                "icon": item["icon_name"],
                "relation": item["relation"],
                "body": item["body"],
                "details": item["details"],
            }
            for item in FeaturedModule.objects.filter(portfolio=portfolio)
            .order_by("order", "id")
            .values("title", "icon_name", "relation", "body", "details")
        ],
        "contactMethods": [
            {
                "label": link["label"],
                "value": link["value"],
                "href": link["href"],
                "icon": link["icon_name"],
            }
            for link in all_links
            if link["type"] == Link.LinkType.CONTACT
        ],
        "footerLinks": [
            {"label": link["label"], "href": link["href"]}
            for link in all_links
            if link["type"] == Link.LinkType.FOOTER
        ],
        "statusPills": [
            {"label": link["label"], "icon": link["icon_name"]}
            for link in all_links
            if link["type"] == Link.LinkType.STATUS
        ],
        "sectionCopy": portfolio.section_copy or {},
        "pageCopy": portfolio.page_copy or {},
    }

class SubmissionReadSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_user_id = serializers.IntegerField(source="owner.id", read_only=True)
    portfolio_id = serializers.IntegerField(source="portfolio.id", read_only=True)
    priority_label = serializers.CharField(source="get_priority_display", read_only=True)

    class Meta:
        model = ContactFormSubmission
        fields = [
            "id", "display_index", "owner_username", "owner_user_id",
            "portfolio_id", "name", "email", "phone", "message",
            "for_work", "priority", "priority_label", "is_dismissed", "submitted_at",
        ]

class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactFormSubmission
        fields = ["name", "email", "phone", "message", "for_work", "priority"]

    def validate_name(self, value: str) -> str:
        val = value.strip()
        if not val:
            raise serializers.ValidationError("Name is required.")
        return val

    def validate_message(self, value: str) -> str:
        val = value.strip()
        if not val:
            raise serializers.ValidationError("Message is required.")
        return val

    def validate_phone(self, value: str | None) -> str | None:
        return value.strip() if value else None

class SubmissionUpdateSerializer(serializers.ModelSerializer):
    display_index = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = ContactFormSubmission
        fields = ["is_dismissed", "priority", "display_index"]

class SubmissionReorderSerializer(serializers.Serializer):
    order = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)

class PortfolioPersonalInfoSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    shortName = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=200)
    subtitle = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    github = serializers.URLField()
    linkedin = serializers.URLField()
    profilePicture = serializers.URLField(required=False, allow_blank=True, allow_null=True)

class PortfolioHeroContentSerializer(serializers.Serializer):
    eyebrow = serializers.CharField(max_length=100)
    title = serializers.CharField()
    description = serializers.CharField()

class PortfolioAboutContentSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()

class PortfolioLinkSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)
    href = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)


class PortfolioHeroActionItemSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)
    href = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)


class PortfolioHeroActionsSerializer(serializers.Serializer):
    primary = PortfolioHeroActionItemSerializer(required=False)
    secondary = PortfolioHeroActionItemSerializer(required=False)

class PortfolioHeroMetricSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=50)
    label = serializers.CharField(max_length=200)


class PortfolioHeroFocusAreaSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)
    value = serializers.IntegerField(min_value=0, max_value=100)


class PortfolioHeroFocusSerializer(serializers.Serializer):
    eyebrow = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    areas = PortfolioHeroFocusAreaSerializer(many=True, default=list)


class PortfolioHeroBadgeSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)


class PortfolioHeroHighlightSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()

class PortfolioSkillGroupSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    items = serializers.ListField(child=serializers.CharField(), default=list)

class PortfolioProjectSerializer(IconAliasSerializer):
    title = serializers.CharField(max_length=200)
    eyebrow = serializers.CharField(max_length=100)
    description = serializers.CharField()
    stack = serializers.ListField(child=serializers.CharField(), default=list)
    stat = serializers.CharField(max_length=100)
    href = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    ctaLabel = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

class PortfolioExperienceSerializer(serializers.Serializer):
    period = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    company = serializers.CharField(max_length=200)
    relation = serializers.CharField(max_length=100)
    summary = serializers.CharField()
    highlights = serializers.ListField(child=serializers.CharField(), default=list)
    relatedComponents = serializers.ListField(child=serializers.CharField(), default=list)

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
    value = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    href = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

class PortfolioStatusPillSerializer(IconAliasSerializer):
    label = serializers.CharField(max_length=100)


class PortfolioSectionCopyEntrySerializer(serializers.Serializer):
    eyebrow = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()


class PortfolioSectionCopySerializer(serializers.Serializer):
    projects = PortfolioSectionCopyEntrySerializer(required=False)
    experience = PortfolioSectionCopyEntrySerializer(required=False)
    components = PortfolioSectionCopyEntrySerializer(required=False)
    contact = PortfolioSectionCopyEntrySerializer(required=False)


class PortfolioPageCopySerializer(serializers.Serializer):
    loadingTitle = serializers.CharField(max_length=200)
    loadingDescription = serializers.CharField()

class PortfolioSubmissionSerializer(serializers.Serializer):
    new_order_index = serializers.IntegerField(min_value=1, required=False, write_only=True)
    is_enabled = serializers.BooleanField(required=False, write_only=True)
    personalInfo = PortfolioPersonalInfoSerializer(required=False)
    navigationLinks = PortfolioLinkSerializer(many=True, required=False, default=list)
    heroContent = PortfolioHeroContentSerializer(required=False)
    heroActions = PortfolioHeroActionsSerializer(required=False)
    heroMetrics = PortfolioHeroMetricSerializer(many=True, required=False, default=list)
    heroFocus = PortfolioHeroFocusSerializer(required=False)
    heroBadges = PortfolioHeroBadgeSerializer(many=True, required=False, default=list)
    heroHighlights = PortfolioHeroHighlightSerializer(many=True, required=False, default=list)
    aboutContent = PortfolioAboutContentSerializer(required=False)
    skillGroups = PortfolioSkillGroupSerializer(many=True, required=False, default=list)
    projects = PortfolioProjectSerializer(many=True, required=False, default=list)
    experience = PortfolioExperienceSerializer(many=True, required=False, default=list)
    showcaseCategories = PortfolioShowcaseCategorySerializer(many=True, required=False, default=list)
    featuredModules = PortfolioFeaturedModuleSerializer(many=True, required=False, default=list)
    contactMethods = PortfolioContactMethodSerializer(many=True, required=False, default=list)
    footerLinks = PortfolioLinkSerializer(many=True, required=False, default=list)
    statusPills = PortfolioStatusPillSerializer(many=True, required=False, default=list)
    sectionCopy = PortfolioSectionCopySerializer(required=False)
    pageCopy = PortfolioPageCopySerializer(required=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            set_serializer_partial(field, self.partial)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        owner = self.context.get("owner")

        if owner and not owner.su_tier:
            restrict_to_3 = [
                ("heroMetrics", "hero metrics"),
                ("skillGroups", "skill groups"),
                ("projects", "projects"),
                ("experience", "experiences"),
                ("showcaseCategories", "showcase categories"),
                ("featuredModules", "featured modules"),
            ]
            
            restrict_to_5 = [
                ("navigationLinks", "navigation links"),
                ("footerLinks", "footer links"),
                ("contactMethods", "contact methods"),
                ("statusPills", "status pills"),
            ]
            
            errors = {}
            for field_key, display_name in restrict_to_3:
                if len(attrs.get(field_key, [])) > 3:
                    errors[field_key] = f"Free tier limit is 3 {display_name}. Upgrade to Premium for unlimited."
                    
            for field_key, display_name in restrict_to_5:
                if len(attrs.get(field_key, [])) > 5:
                    errors[field_key] = f"Free tier limit is 5 {display_name}."
                    
            if errors:
                raise serializers.ValidationError(errors)

        return attrs

    @transaction.atomic
    def save(self, **kwargs: Any) -> PortfolioSettings:
        owner = kwargs.get("owner") or self.context.get("owner")
        order_index = self.context.get("order_index", 1)
        
        if not owner:
            raise ValueError("PortfolioSubmissionSerializer.save() requires an owner.")

        existing = PortfolioSettings.objects.filter(owner=owner, order_index=order_index).first()
        current_data = serialize_portfolio_payload(existing) if existing else {}
        data = deep_merge_portfolio_data(current_data, self.validated_data)

        required_on_create = ["personalInfo", "heroContent", "aboutContent"]
        if not existing:
            missing = [field for field in required_on_create if field not in data]
            if missing:
                raise serializers.ValidationError(
                    {field: "This field is required when creating a portfolio." for field in missing}
                )

        pi = data["personalInfo"]
        hc = data["heroContent"]
        ac = data["aboutContent"]

        portfolio, created = PortfolioSettings.objects.get_or_create(
            owner=owner,
            order_index=order_index,
            defaults={"short_name": pi["shortName"], "title": pi["title"], "subtitle": pi["subtitle"], "location": pi["location"], "email": pi["email"], "github": pi["github"], "linkedin": pi["linkedin"], "hero_eyebrow": hc["eyebrow"], "hero_title": hc["title"], "hero_description": hc["description"], "about_title": ac["title"], "about_description": ac["description"]},
        )
        if created:
            portfolio.name = pi["name"]

        portfolio.name = pi["name"]
        portfolio.short_name = pi["shortName"]
        portfolio.title = pi["title"]
        portfolio.subtitle = pi["subtitle"]
        portfolio.location = pi["location"]
        portfolio.email = pi["email"]
        portfolio.github = pi["github"]
        portfolio.linkedin = pi["linkedin"]
        portfolio.hero_eyebrow = hc["eyebrow"]
        portfolio.hero_title = hc["title"]
        portfolio.hero_description = hc["description"]
        portfolio.hero_actions = data.get("heroActions", portfolio.hero_actions)
        portfolio.hero_focus = data.get("heroFocus", portfolio.hero_focus)
        portfolio.hero_badges = data.get("heroBadges", portfolio.hero_badges)
        portfolio.hero_highlights = data.get("heroHighlights", portfolio.hero_highlights)
        portfolio.about_title = ac["title"]
        portfolio.about_description = ac["description"]
        portfolio.section_copy = data.get("sectionCopy", portfolio.section_copy)
        portfolio.page_copy = data.get("pageCopy", portfolio.page_copy)
        portfolio.tier = owner.tier
        if "is_enabled" in data:
            portfolio.is_enabled = data["is_enabled"]
        portfolio.save()

        profile_picture = pi.get("profilePicture")
        if profile_picture is not None and owner.profile_picture_url != profile_picture:
            owner.profile_picture_url = profile_picture
            owner.save(update_fields=["profile_picture_url"])

        mapping = [
            (HeroMetric, data.get("heroMetrics"), lambda x: x),
            (SkillGroup, data.get("skillGroups"), lambda x: x),
            (Project, data.get("projects"), lambda x: {
                "title": x["title"],
                "eyebrow": x["eyebrow"],
                "description": x["description"],
                "stack": x["stack"],
                "stat": x["stat"],
                "href": x.get("href"),
                "cta_label": x.get("ctaLabel"),
                "icon_name": x.get("icon"),
            }),
            (Experience, data.get("experience"), lambda x: {
                "period": x["period"], "title": x["title"], "company": x["company"],
                "relation": x["relation"], "summary": x["summary"], "highlights": x["highlights"],
                "related_components": x["relatedComponents"]
            }),
            (ShowcaseCategory, data.get("showcaseCategories"), lambda x: {
                "title": x["title"], "icon_name": x["icon"], "relation": x["relation"],
                "preview": x["preview"], "items": x["items"]
            }),
            (FeaturedModule, data.get("featuredModules"), lambda x: {
                "title": x["title"], "icon_name": x["icon"], "relation": x["relation"],
                "body": x["body"], "details": x["details"]
            }),
        ]

        for model, items, parser in mapping:
            if items is None:
                continue
            model.objects.filter(portfolio=portfolio).delete()
            model.objects.bulk_create([model(portfolio=portfolio, order=idx, **parser(item)) for idx, item in enumerate(items, 1)])

        link_types = [
            (Link.LinkType.NAV, data.get("navigationLinks")),
            (Link.LinkType.CONTACT, data.get("contactMethods")),
            (Link.LinkType.FOOTER, data.get("footerLinks")),
            (Link.LinkType.STATUS, data.get("statusPills")),
        ]
        
        all_links = []
        for l_type, items in link_types:
            if items is None:
                continue
            Link.objects.filter(portfolio=portfolio, type=l_type).delete()
            all_links.extend([
                Link(portfolio=portfolio, order=idx, type=l_type, label=item["label"], 
                     value=item.get("value"), href=item.get("href"), icon_name=item.get("icon"))
                for idx, item in enumerate(items, 1)
            ])
        if all_links:
            Link.objects.bulk_create(all_links)

        return portfolio