import secrets

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Max


def generate_share_token():
    return secrets.token_urlsafe(24)


# Kept for migration compatibility with older schema history.
def generate_dashboard_token():
    return secrets.token_urlsafe(32)


class User(AbstractUser):
    class Tier(models.IntegerChoices):
        FREE = 0, "Free"
        PRO = 1, "Pro"
        PREMIUM = 2, "Premium"

    # Standard Manager for Custom User models
    objects = UserManager()

    # Core Identity Fields
    email = models.EmailField(unique=True, help_text="Primary identifier for login and OTP.")
    tier = models.IntegerField(choices=Tier.choices, default=Tier.FREE)
    
    # Verification & Security State
    is_verified = models.BooleanField(
        default=False, 
        help_text="Designates whether the user has verified their email via OTP."
    )
    
    # Portfolio Sharing Controls
    enable_share_token = models.BooleanField(
        default=False,
        help_text="Toggle to make the portfolio publicly accessible via the share_token."
    )
    share_token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_share_token,
        editable=False,
        help_text="The unique slug used in the public portfolio URL."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Properties for Logic Checks ---

    @property
    def is_free_tier(self):
        return self.tier == self.Tier.FREE

    @property
    def su_tier(self):
        """
        Returns True if user is a Superuser OR a paying customer.
        Used to bypass rate limits or item count restrictions.
        """
        return self.is_superuser or self.tier != self.Tier.FREE

    # --- Validation & Integrity ---

    def clean(self):
        """
        Custom validation to enforce the 'Verified-to-Share' rule.
        This prevents sharing from being enabled via Django Admin by accident.
        """
        super().clean()
        if self.enable_share_token and not self.is_verified:
            raise ValidationError({
                'enable_share_token': "A user must be verified before they can enable portfolio sharing."
            })

    def save(self, *args, **kwargs):
        """
        Overriding save to ensure full_clean is called, running our 
        validation logic even outside of Django Forms.
        """
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
    class Tier(models.IntegerChoices):
        FREE = 0, "Free"
        PRO = 1, "Pro"
        PREMIUM = 2, "Premium"

    objects = UserManager()

    email = models.EmailField(unique=True)
    tier = models.IntegerField(choices=Tier.choices, default=Tier.FREE)
    is_verified = models.BooleanField(default=False)
    enable_share_token = models.BooleanField(default=False)
    share_token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_share_token,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_free_tier(self):
        return self.tier == self.Tier.FREE

    @property
    def su_tier(self):
        return self.is_superuser or not self.is_free_tier

    def __str__(self):
        return self.username


class OwnedPortfolioModel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True


class OrderedPortfolioModel(OwnedPortfolioModel):
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class ContactFormSubmission(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 0, "Low"
        MEDIUM = 1, "Medium"
        HIGH = 2, "High"
        URGENT = 3, "Urgent"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    portfolio = models.ForeignKey(
        "PortfolioSettings",
        on_delete=models.SET_NULL,
        related_name="submissions",
        blank=True,
        null=True,
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

    def save(self, *args, **kwargs):
        if self._state.adding and not self.display_index:
            max_index = (
                ContactFormSubmission.objects.filter(owner=self.owner)
                .aggregate(max_index=Max("display_index"))
                .get("max_index")
            )
            self.display_index = (max_index or 0) + 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def move_to_index(self, new_index):
        owner_submissions = list(
            ContactFormSubmission.objects.select_for_update()
            .filter(owner=self.owner)
            .order_by("display_index", "id")
        )
        total = len(owner_submissions)
        new_index = max(1, min(int(new_index), total))

        if new_index == self.display_index:
            return

        moving_submission = next(
            submission for submission in owner_submissions if submission.pk == self.pk
        )
        reordered = [
            submission for submission in owner_submissions if submission.pk != self.pk
        ]
        reordered.insert(new_index - 1, moving_submission)

        offset = total + 1000
        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index + offset
            submission.save(update_fields=["display_index"])

        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index
            submission.save(update_fields=["display_index"])

        self.display_index = new_index

    @classmethod
    @transaction.atomic
    def reorder_for_owner(cls, owner, ordered_ids):
        owner_submissions = list(
            cls.objects.select_for_update()
            .filter(owner=owner)
            .order_by("display_index", "id")
        )

        if not ordered_ids:
            return owner_submissions

        current_ids = [submission.id for submission in owner_submissions]
        if sorted(current_ids) != sorted(ordered_ids):
            raise ValueError("Order must include each submission exactly once.")

        id_to_submission = {submission.id: submission for submission in owner_submissions}
        reordered = [id_to_submission[submission_id] for submission_id in ordered_ids]
        offset = len(reordered) + 1000

        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index + offset
            submission.save(update_fields=["display_index"])

        for index, submission in enumerate(reordered, start=1):
            submission.display_index = index
            submission.save(update_fields=["display_index"])

        return reordered

    def __str__(self):
        return (
            f"{self.name} - {self.email} - {self.owner.username} - "
            f"{self.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class PortfolioSettings(OwnedPortfolioModel):
    name = models.CharField(max_length=100, default="Soham Dutta")
    short_name = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    github = models.URLField()
    linkedin = models.URLField()
    hero_eyebrow = models.CharField(max_length=100)
    hero_title = models.TextField()
    hero_description = models.TextField()
    about_title = models.CharField(max_length=200)
    about_description = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner"],
                name="unique_portfolio_settings_per_owner",
            )
        ]
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def clean(self):
        if (
            self.owner_id
            and PortfolioSettings.objects.exclude(pk=self.pk)
            .filter(owner=self.owner)
            .exists()
        ):
            raise ValidationError(
                "Each owner can only have one portfolio record."
            )

    def __str__(self):
        return f"{self.owner.username}'s Portfolio"

    @property
    def share_token(self):
        return self.owner.share_token


class HeroMetric(OrderedPortfolioModel):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=200)


class SkillGroup(OrderedPortfolioModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    items = models.JSONField(default=list, help_text="List of skill strings")


class Project(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    eyebrow = models.CharField(max_length=100)
    description = models.TextField()
    stat = models.CharField(max_length=100)
    stack = models.JSONField(default=list, help_text="List of tech stack strings")


class Experience(OrderedPortfolioModel):
    MAX_FREE_TIER_EXPERIENCES = 3
    FREE_TIER_LIMIT_MESSAGE = (
        f"Free tier users can only add up to {MAX_FREE_TIER_EXPERIENCES} experiences."
    )

    period = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    summary = models.TextField()
    highlights = models.JSONField(default=list)
    related_components = models.JSONField(default=list)

    def clean(self):
        super().clean()

        if not self.owner_id or self.owner.su_tier:
            return

        existing_count = Experience.objects.filter(owner=self.owner).exclude(
            pk=self.pk
        ).count()
        if existing_count >= self.MAX_FREE_TIER_EXPERIENCES:
            raise ValidationError(self.FREE_TIER_LIMIT_MESSAGE)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ShowcaseCategory(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50, help_text="Lucide icon component name")
    relation = models.CharField(max_length=100)
    preview = models.TextField()
    items = models.JSONField(default=list)

    class Meta(OrderedPortfolioModel.Meta):
        verbose_name_plural = "Showcase Categories"


class FeaturedModule(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50)
    relation = models.CharField(max_length=100)
    body = models.TextField()
    details = models.TextField()


class Link(OrderedPortfolioModel):
    class LinkType(models.TextChoices):
        NAV = "NAV", "Navigation"
        FOOTER = "FOOTER", "Footer"
        CONTACT = "CONTACT", "Contact Method"
        STATUS = "STATUS", "Status Pill"

    type = models.CharField(max_length=20, choices=LinkType.choices)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200, blank=True, null=True)
    href = models.CharField(max_length=200, blank=True, null=True)
    icon_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta(OrderedPortfolioModel.Meta):
        ordering = ["type", "order", "id"]
