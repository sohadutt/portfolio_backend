from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from .models import (
    ContactFormSubmission, Experience, FeaturedModule, HeroMetric,
    Link, PortfolioSettings, Project, ShowcaseCategory, SkillGroup, User,
)

# --- USER SERIALIZERS ---

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

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email=email, is_verified=True).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.pop("password")
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults=validated_data
        )

        if not created:
            for attr, value in validated_data.items():
                setattr(user, attr, value)

        user.set_password(password)
        user.is_verified = True
        user.save()
        return user

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture", "theme_mode"]

    def validate_profile_picture(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image size must be under 2MB.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture_url"]

# --- AUTH & UTILITY SERIALIZERS ---

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
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

    def validate(self, attrs):
        attrs["icon"] = attrs.get("icon") or attrs.get("iconName")
        return attrs

# --- SUBMISSION SERIALIZERS ---

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

    def validate_name(self, value):
        val = value.strip()
        if not val: raise serializers.ValidationError("Name is required.")
        return val

    def validate_message(self, value):
        val = value.strip()
        if not val: raise serializers.ValidationError("Message is required.")
        return val

    def validate_phone(self, value):
        return value.strip() if value else None

class SubmissionUpdateSerializer(serializers.ModelSerializer):
    display_index = serializers.IntegerField(min_value=1, required=False)

    class Meta:
        model = ContactFormSubmission
        fields = ["is_dismissed", "priority", "display_index"]

class SubmissionReorderSerializer(serializers.Serializer):
    order = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=False)

# --- PORTFOLIO COMPONENTS ---

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
    href = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

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

# --- MAIN SUBMISSION SERIALIZER ---

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
        
        # Enforce Free Tier Array Limits
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
    def save(self, **kwargs):
        owner = kwargs.get("owner") or self.context.get("owner")
        order_index = self.context.get("order_index", 1)
        
        if not owner:
            raise ValueError("PortfolioSubmissionSerializer.save() requires an owner.")

        data = self.validated_data
        pi, hc, ac = data["personalInfo"], data["heroContent"], data["aboutContent"]

        portfolio, _ = PortfolioSettings.objects.update_or_create(
            owner=owner,
            order_index=order_index,
            defaults={
                "name": pi["name"], "short_name": pi["shortName"], "title": pi["title"],
                "subtitle": pi["subtitle"], "location": pi["location"], "email": pi["email"],
                "github": pi["github"], "linkedin": pi["linkedin"],
                "hero_eyebrow": hc["eyebrow"], "hero_title": hc["title"], "hero_description": hc["description"],
                "about_title": ac["title"], "about_description": ac["description"],
                "tier": owner.tier # Cascade current tier state to the portfolio record
            },
        )

        # Mapping for efficient updates - Attach to PORTFOLIO instead of owner
        mapping = [
            (HeroMetric, data["heroMetrics"], lambda x: x),
            (SkillGroup, data["skillGroups"], lambda x: x),
            (Project, data["projects"], lambda x: x),
            (Experience, data["experience"], lambda x: {
                "period": x["period"], "title": x["title"], "company": x["company"],
                "relation": x["relation"], "summary": x["summary"], "highlights": x["highlights"],
                "related_components": x["relatedComponents"]
            }),
            (ShowcaseCategory, data["showcaseCategories"], lambda x: {
                "title": x["title"], "icon_name": x["icon"], "relation": x["relation"],
                "preview": x["preview"], "items": x["items"]
            }),
            (FeaturedModule, data["featuredModules"], lambda x: {
                "title": x["title"], "icon_name": x["icon"], "relation": x["relation"],
                "body": x["body"], "details": x["details"]
            }),
        ]

        for model, items, parser in mapping:
            model.objects.filter(portfolio=portfolio).delete()
            model.objects.bulk_create([model(portfolio=portfolio, order=idx, **parser(item)) for idx, item in enumerate(items, 1)])

        # Handle Links - Attach to PORTFOLIO
        Link.objects.filter(portfolio=portfolio).delete()
        link_types = [
            (Link.LinkType.NAV, data["navigationLinks"]),
            (Link.LinkType.CONTACT, data["contactMethods"]),
            (Link.LinkType.FOOTER, data["footerLinks"]),
            (Link.LinkType.STATUS, data["statusPills"]),
        ]
        
        all_links = []
        for l_type, items in link_types:
            all_links.extend([
                Link(portfolio=portfolio, order=idx, type=l_type, label=item["label"], 
                     value=item.get("value"), href=item.get("href"), icon_name=item.get("icon"))
                for idx, item in enumerate(items, 1)
            ])
        if all_links:
            Link.objects.bulk_create(all_links)

        return portfolio