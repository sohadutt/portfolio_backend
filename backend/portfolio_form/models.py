from __future__ import annotations

import secrets
from typing import Any, TypeAlias, TypedDict

import vercel_blob
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import post_delete
from django.dispatch import receiver

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]


class HeroActionConfig(TypedDict, total=False):
    label: str
    href: str


class HeroActionsConfig(TypedDict, total=False):
    primary: HeroActionConfig
    secondary: HeroActionConfig


class HeroFocusAreaConfig(TypedDict, total=False):
    label: str
    value: int
    icon: str


class HeroFocusConfig(TypedDict, total=False):
    eyebrow: str
    title: str
    areas: list[HeroFocusAreaConfig]


class SectionCopyEntryConfig(TypedDict, total=False):
    eyebrow: str
    title: str
    description: str


class SectionCopyConfig(TypedDict, total=False):
    projects: SectionCopyEntryConfig
    experience: SectionCopyEntryConfig
    components: SectionCopyEntryConfig
    contact: SectionCopyEntryConfig


class PageCopyConfig(TypedDict, total=False):
    loadingTitle: str
    loadingDescription: str


def generate_share_token() -> str:
    return secrets.token_urlsafe(24)


def generate_dashboard_token() -> str:
    return secrets.token_urlsafe(32)


def default_hero_actions() -> HeroActionsConfig:
    return {
        "primary": {"label": "", "href": ""},
        "secondary": {"label": "", "href": ""},
    }


def default_hero_focus() -> HeroFocusConfig:
    return {
        "eyebrow": "",
        "title": "",
        "areas": [],
    }


def default_section_copy() -> SectionCopyConfig:
    return {
        "projects": {"eyebrow": "", "title": "", "description": ""},
        "experience": {"eyebrow": "", "title": "", "description": ""},
        "components": {"eyebrow": "", "title": "", "description": ""},
        "contact": {"eyebrow": "", "title": "", "description": ""},
    }


def default_page_copy() -> PageCopyConfig:
    return {
        "loadingTitle": "",
        "loadingDescription": "",
    }


class User(AbstractUser):
    class Tier(models.IntegerChoices):
        FREE = 0, "Free"
        PRO = 1, "Pro"
        PREMIUM = 2, "Premium"

    class ThemeMode(models.IntegerChoices):
        OCEAN = 0, "Ocean"
        FOREST = 1, "Forest"
        DESERT = 2, "Desert"
        SPACE = 3, "Space"
        SUNSET = 4, "Sunset"

    objects = UserManager()

    email = models.EmailField(unique=True, help_text="Primary identifier for login and OTP.")
    tier = models.IntegerField(choices=Tier.choices, default=Tier.FREE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile_picture_url = models.URLField(max_length=500, null=True, blank=True)
    theme_mode = models.IntegerField(choices=ThemeMode.choices, default=ThemeMode.OCEAN)
    is_verified = models.BooleanField(
        default=False, 
        help_text="Designates whether the user has verified their email via OTP."
    )
    enable_share_token = models.BooleanField(
        default=False,
        help_text="Toggle to make the portfolio publicly accessible."
    )
    share_token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_share_token,
        editable=False,
        help_text="The unique slug used in the public portfolio URL."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_free_tier(self) -> bool:
        return self.tier == self.Tier.FREE

    @property
    def su_tier(self) -> bool:
        return self.is_superuser or self.tier != self.Tier.FREE

    def clean(self) -> None:
        super().clean()
        if self.enable_share_token and not self.is_verified:
            raise ValidationError({
                'enable_share_token': "A user must be verified before they can enable portfolio sharing."
            })

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.pk:
            try:
                old_obj = User.objects.get(pk=self.pk)
                if old_obj.profile_picture_url and old_obj.profile_picture_url != self.profile_picture_url:
                    if "vercel-storage.com" in old_obj.profile_picture_url:
                        vercel_blob.delete(old_obj.profile_picture_url)
            except (User.DoesNotExist, Exception):
                pass

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']


@receiver(post_delete, sender=User)
def auto_delete_user_blob_on_delete(sender: type[User], instance: User, **kwargs: Any) -> None:
    """Automatically cleans up Vercel Blob storage if a user profile is deleted."""
    if instance.profile_picture_url and "vercel-storage.com" in instance.profile_picture_url:
        try:
            vercel_blob.delete(instance.profile_picture_url)
        except Exception:
            pass


class OwnedPortfolioModel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True


class OrderedPortfolioModel(models.Model):
    MAX_FREE_TIER_ITEMS = 3

    portfolio = models.ForeignKey(
        'PortfolioSettings',
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ["order", "id"]

    def clean(self) -> None:
        super().clean()
        if self.portfolio_id and hasattr(self.portfolio, 'owner') and not self.portfolio.owner.su_tier:
            count = self.__class__.objects.filter(portfolio=self.portfolio).exclude(pk=self.pk).count()
            if count >= self.MAX_FREE_TIER_ITEMS:
                raise ValidationError(f"Free tier limit is {self.MAX_FREE_TIER_ITEMS} items. Please upgrade to Premium.")

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class ContactFormSubmission(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 0, "Low"
        MEDIUM = 1, "Medium"
        HIGH = 2, "High"
        URGENT = 3, "Urgent"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    portfolio = models.ForeignKey(
        "PortfolioSettings",
        on_delete=models.SET_NULL,
        related_name="submissions",
        blank=True, null=True,
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    for_work = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    is_dismissed = models.BooleanField(default=False)
    display_index = models.PositiveIntegerField()

    class Meta:
        ordering = ["display_index", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "display_index"],
                name="unique_submission_index_per_owner",
            )
        ]

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.display_index:
            max_idx = ContactFormSubmission.objects.filter(owner=self.owner).aggregate(Max("display_index"))["display_index__max"]
            self.display_index = (max_idx or 0) + 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def move_to_index(self, new_index: int) -> None:
        submissions = list(ContactFormSubmission.objects.select_for_update().filter(owner=self.owner).order_by("display_index", "id"))
        new_index = max(1, min(int(new_index), len(submissions)))
        
        if new_index == self.display_index:
            return

        moving = next(s for s in submissions if s.pk == self.pk)
        rem = [s for s in submissions if s.pk != self.pk]
        rem.insert(new_index - 1, moving)

        for i, s in enumerate(rem, 1):
            s.display_index = i + 10000 
            s.save(update_fields=["display_index"])
        for i, s in enumerate(rem, 1):
            s.display_index = i
            s.save(update_fields=["display_index"])

    @classmethod
    @transaction.atomic
    def reorder_for_owner(cls, owner: User, ordered_ids: list[int]) -> list["ContactFormSubmission"]:
        submissions = {s.id: s for s in cls.objects.select_for_update().filter(owner=owner)}
        if sorted(submissions.keys()) != sorted(ordered_ids):
            raise ValueError("Invalid ID list for reordering.")

        reordered = [submissions[sid] for sid in ordered_ids]
        for i, s in enumerate(reordered, 1):
            s.display_index = i + 10000
            s.save(update_fields=["display_index"])
        for i, s in enumerate(reordered, 1):
            s.display_index = i
            s.save(update_fields=["display_index"])
        return reordered


class PortfolioSettings(OwnedPortfolioModel):
    order_index = models.PositiveIntegerField(default=1)
    is_enabled = models.BooleanField(default=True)
    tier = models.IntegerField(choices=User.Tier.choices, default=User.Tier.FREE)

    name = models.CharField(max_length=100, default="Soham Dutta")
    short_name = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    hero_eyebrow = models.CharField(max_length=100, blank=True, null=True)
    hero_title = models.TextField(blank=True, null=True)
    hero_description = models.TextField(blank=True, null=True)
    hero_actions = models.JSONField(default=default_hero_actions)
    hero_focus = models.JSONField(default=default_hero_focus)
    hero_badges = models.JSONField(default=list)
    hero_highlights = models.JSONField(default=list)
    about_title = models.CharField(max_length=200, blank=True, null=True)
    about_description = models.TextField(blank=True, null=True)
    section_copy = models.JSONField(default=default_section_copy)
    page_copy = models.JSONField(default=default_page_copy)
    
    # Portfolio-specific resume
    resume_url = models.URLField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "order_index"], name="unique_portfolio_settings_per_owner_index")
        ]
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def clean(self) -> None:
        if self.owner_id and self.order_index > 1 and self.owner.tier == User.Tier.FREE:
            raise ValidationError("Free tier users can only have one portfolio.")

    @transaction.atomic
    def move_to_index(self, new_index: int) -> None:
        portfolios = list(
            PortfolioSettings.objects.select_for_update()
            .filter(owner=self.owner)
            .order_by("order_index")
        )

        new_index = max(1, min(int(new_index), len(portfolios)))

        if new_index == self.order_index:
            return

        moving = next(p for p in portfolios if p.pk == self.pk)
        rem = [p for p in portfolios if p.pk != self.pk]
        rem.insert(new_index - 1, moving)

        for i, p in enumerate(rem, 1):
            p.order_index = i + 10000
            p.save(update_fields=["order_index"])

        for i, p in enumerate(rem, 1):
            p.order_index = i
            p.save(update_fields=["order_index"])

    def __str__(self) -> str:
        return f"{self.owner.username}'s Portfolio #{self.order_index}"

    @property
    def share_token(self) -> str:
        return self.owner.share_token


@receiver(post_delete, sender=PortfolioSettings)
def auto_delete_portfolio_resume_on_delete(sender: type[PortfolioSettings], instance: PortfolioSettings, **kwargs: Any) -> None:
    """Automatically cleans up Vercel Blob storage if a portfolio containing a resume is deleted."""
    if instance.resume_url and "vercel-storage.com" in instance.resume_url:
        try:
            vercel_blob.delete(instance.resume_url)
        except Exception:
            pass


class HeroMetric(OrderedPortfolioModel):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")

class SkillGroup(OrderedPortfolioModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    items = models.JSONField(default=list)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")

class Project(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    eyebrow = models.CharField(max_length=100)
    description = models.TextField()
    stat = models.CharField(max_length=100)
    stack = models.JSONField(default=list)
    href = models.CharField(max_length=255, blank=True, null=True, help_text="Target URL or anchor link")
    cta_label = models.CharField(max_length=100, blank=True, null=True, help_text="Text to display on the action button")
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name string")

class Experience(OrderedPortfolioModel):
    period = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    summary = models.TextField()
    highlights = models.JSONField(default=list)
    related_components = models.JSONField(default=list)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")

class ShowcaseCategory(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")
    relation = models.CharField(max_length=100)
    preview = models.TextField()
    items = models.JSONField(default=list)
    class Meta(OrderedPortfolioModel.Meta):
        verbose_name_plural = "Showcase Categories"

class FeaturedModule(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")
    relation = models.CharField(max_length=100)
    body = models.TextField()
    details = models.TextField()

class Link(OrderedPortfolioModel):
    MAX_FREE_TIER_ITEMS = 3
    
    class LinkType(models.TextChoices):
        NAV = "NAV", "Navigation"
        FOOTER = "FOOTER", "Footer"
        CONTACT = "CONTACT", "Contact Method"
        STATUS = "STATUS", "Status Pill"

    type = models.CharField(max_length=20, choices=LinkType.choices)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200, blank=True, null=True)
    href = models.CharField(max_length=200, blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True, help_text="Lucide icon name")