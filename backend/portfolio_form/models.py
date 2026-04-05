import secrets
import vercel_blob
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import post_delete
from django.dispatch import receiver

# --- Utility Functions ---

def generate_share_token():
    return secrets.token_urlsafe(24)

def generate_dashboard_token():
    """Kept for migration compatibility."""
    return secrets.token_urlsafe(32)

# --- Core User Model ---

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

    # Identity & Profile
    email = models.EmailField(unique=True, help_text="Primary identifier for login and OTP.")
    tier = models.IntegerField(choices=Tier.choices, default=Tier.FREE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    profile_picture_url = models.URLField(max_length=500, null=True, blank=True)
    theme_mode = models.IntegerField(choices=ThemeMode.choices, default=ThemeMode.OCEAN)
    
    # Verification State
    is_verified = models.BooleanField(
        default=False, 
        help_text="Designates whether the user has verified their email via OTP."
    )
    
    # Portfolio Sharing
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
    def is_free_tier(self):
        return self.tier == self.Tier.FREE

    @property
    def su_tier(self):
        """Returns True if user is a Superuser OR a paying customer."""
        return self.is_superuser or self.tier != self.Tier.FREE

    def clean(self):
        super().clean()
        if self.enable_share_token and not self.is_verified:
            raise ValidationError({
                'enable_share_token': "A user must be verified before they can enable portfolio sharing."
            })

    def save(self, *args, **kwargs):
        # Handle cleanup of old profile picture if the URL is being changed
        if self.pk:
            try:
                old_obj = User.objects.get(pk=self.pk)
                if old_obj.profile_picture_url and old_obj.profile_picture_url != self.profile_picture_url:
                    vercel_blob.delete(old_obj.profile_picture_url)
            except (User.DoesNotExist, Exception):
                pass

        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Capture URL before deletion for the signal/manual cleanup
        url_to_delete = self.profile_picture_url
        super().delete(*args, **kwargs)
        if url_to_delete:
            try:
                vercel_blob.delete(url_to_delete)
            except Exception:
                pass

    def __str__(self):
        return f"{self.username} ({self.email})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

# --- Global Signals ---

@receiver(post_delete, sender=User)
def auto_delete_vercel_blob_on_delete(sender, instance, **kwargs):
    """Safety net: ensures the blob is deleted when a user is removed."""
    if instance.profile_picture_url:
        try:
            vercel_blob.delete(instance.profile_picture_url)
        except Exception:
            pass

# --- Base Abstract Models ---

class OwnedPortfolioModel(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )
    class Meta:
        abstract = True

class OrderedPortfolioModel(models.Model):
    MAX_FREE_TIER_ITEMS = 3 # Global default limit for free tier

    portfolio = models.ForeignKey(
        'PortfolioSettings',
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ["order", "id"]

    def clean(self):
        super().clean()
        # Enforce the limit for Free Tier users
        if self.portfolio_id and hasattr(self.portfolio, 'owner') and not self.portfolio.owner.su_tier:
            count = self.__class__.objects.filter(portfolio=self.portfolio).exclude(pk=self.pk).count()
            if count >= self.MAX_FREE_TIER_ITEMS:
                raise ValidationError(f"Free tier limit is {self.MAX_FREE_TIER_ITEMS} items. Please upgrade to Premium.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# --- Functional Portfolio Models ---

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

    def save(self, *args, **kwargs):
        if not self.display_index:
            max_idx = ContactFormSubmission.objects.filter(owner=self.owner).aggregate(Max("display_index"))["display_index__max"]
            self.display_index = (max_idx or 0) + 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def move_to_index(self, new_index):
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
    def reorder_for_owner(cls, owner, ordered_ids):
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
    # NEW FIELDS FOR MULTI-PORTFOLIO SUPPORT
    order_index = models.PositiveIntegerField(default=1)
    is_enabled = models.BooleanField(default=True)
    tier = models.IntegerField(choices=User.Tier.choices, default=User.Tier.FREE)

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
            # Allow multiple portfolios per user, separated by their order_index
            models.UniqueConstraint(fields=["owner", "order_index"], name="unique_portfolio_settings_per_owner_index")
        ]
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def clean(self):
        # Enforce free tier limitations
        if self.owner_id and self.order_index > 1 and self.owner.tier == User.Tier.FREE:
            raise ValidationError("Free tier users can only have one portfolio.")

    @transaction.atomic
    def move_to_index(self, new_index):
        """Safely shifts portfolios to maintain a continuous 1-based index."""
        portfolios = list(
            PortfolioSettings.objects.select_for_update()
            .filter(owner=self.owner)
            .order_by("order_index")
        )
        
        # Ensure we don't move it out of bounds
        new_index = max(1, min(int(new_index), len(portfolios)))
        
        if new_index == self.order_index:
            return

        # Pop the moving portfolio and insert it at the new position
        moving = next(p for p in portfolios if p.pk == self.pk)
        rem = [p for p in portfolios if p.pk != self.pk]
        rem.insert(new_index - 1, moving)

        # Step 1: Temporary shift (+10000) to avoid UniqueConstraint collisions during save
        for i, p in enumerate(rem, 1):
            p.order_index = i + 10000
            p.save(update_fields=["order_index"])
            
        # Step 2: Set the final correct sequential indices
        for i, p in enumerate(rem, 1):
            p.order_index = i
            p.save(update_fields=["order_index"])

    def __str__(self):
        return f"{self.owner.username}'s Portfolio #{self.order_index}"

    @property
    def share_token(self):
        return self.owner.share_token

class HeroMetric(OrderedPortfolioModel):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=200)

class SkillGroup(OrderedPortfolioModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    items = models.JSONField(default=list)

class Project(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    eyebrow = models.CharField(max_length=100)
    description = models.TextField()
    stat = models.CharField(max_length=100)
    stack = models.JSONField(default=list)

class Experience(OrderedPortfolioModel):
    period = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    relation = models.CharField(max_length=100)
    summary = models.TextField()
    highlights = models.JSONField(default=list)
    related_components = models.JSONField(default=list)

class ShowcaseCategory(OrderedPortfolioModel):
    title = models.CharField(max_length=200)
    icon_name = models.CharField(max_length=50, help_text="Lucide icon name")
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
    # Override the default 3 limit so navbars and footers don't break for free users
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
    icon_name = models.CharField(max_length=50, blank=True, null=True)