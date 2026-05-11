import io
import secrets
import vercel_blob
from PIL import Image
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html

from .models import (
    User, PortfolioSettings, ContactFormSubmission, 
    HeroMetric, SkillGroup, Project, Experience, 
    ShowcaseCategory, FeaturedModule, Link
)

# ==========================================
# 1. UTILITIES & FORMS
# ==========================================

def get_compressed_webp_buffer(uploaded_file, quality=80):
    """
    Converts any uploaded image to a compressed WebP byte stream.
    Used to optimize profile pictures before sending them to Vercel.
    """
    img = Image.open(uploaded_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="WEBP", quality=quality, method=6)
    buffer.seek(0)
    return buffer

class UserAdminForm(forms.ModelForm):
    """Custom form to handle image uploads cleanly in the Admin UI."""
    upload_profile_picture = forms.ImageField(
        required=False, 
        help_text="Upload a new photo. Old photos will be automatically deleted from Vercel."
    )

    class Meta:
        model = User
        fields = '__all__'


# ==========================================
# 2. INLINES FOR PORTFOLIO EDITING
# ==========================================
# These classes allow you to edit a user's projects, skills, etc., 
# directly on the PortfolioSettings admin page without switching tabs.

class HeroMetricInline(admin.TabularInline):
    model = HeroMetric
    extra = 0

class SkillGroupInline(admin.TabularInline):
    model = SkillGroup
    extra = 0

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0

class ShowcaseCategoryInline(admin.TabularInline):
    model = ShowcaseCategory
    extra = 0

class FeaturedModuleInline(admin.TabularInline):
    model = FeaturedModule
    extra = 0

class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


# ==========================================
# 3. MAIN ADMIN REGISTRATIONS
# ==========================================

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Manages custom User attributes, tiers, and handles Vercel Blob 
    profile picture uploads directly from the Django Admin interface.
    """
    form = UserAdminForm
    list_display = ("id", "username", "email", "tier", "is_verified", "profile_preview", "is_staff")
    readonly_fields = ("share_token", "created_at", "profile_preview")
    
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Portfolio & Identity", {
            "fields": (
                "tier", "theme_mode", "is_verified", "upload_profile_picture",
                "profile_picture_url", "profile_preview", "enable_share_token", 
                "share_token", "created_at"
            )
        }),
    )

    def profile_preview(self, obj):
        """Renders a circular HTML preview of the user's avatar in the admin panel."""
        if obj.profile_picture_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; '
                'object-fit: cover; border: 1px solid #ccc;" />',
                obj.profile_picture_url
            )
        return "No Image"
    profile_preview.short_description = "Avatar Preview"

    def save_model(self, request, obj, form, change):
        """Intercepts the save to handle file compression and Vercel upload."""
        upload_file = form.cleaned_data.get("upload_profile_picture")
        if upload_file:
            old_url = None
            if change:
                try:
                    old_url = User.objects.get(pk=obj.pk).profile_picture_url
                except User.DoesNotExist: pass

            try:
                webp_buffer = get_compressed_webp_buffer(upload_file)
                random_suffix = secrets.token_hex(3)
                filename = f"u{obj.username}_{random_suffix}.webp"
                
                blob_resp = vercel_blob.put(
                    path=f"profile_pics/{filename}",
                    data=webp_buffer.read(),
                    options={"access": "public", "content_type": "image/webp"}
                )
                obj.profile_picture_url = blob_resp["url"]
                
                if old_url:
                    try: vercel_blob.delete(old_url)
                    except Exception:
                        self.message_user(request, "New photo saved, but old cleanup failed.", level="WARNING")
            except Exception as e:
                self.message_user(request, f"Image Upload Failed: {str(e)}", level="ERROR")
        
        super().save_model(request, obj, form, change)


@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(admin.ModelAdmin):
    """
    Central hub for managing a specific portfolio. Uses inlines to allow
    editing of all related projects and experiences on the same page.
    """
    list_display = ("owner", "order_index", "is_enabled", "tier", "name", "title")
    list_filter = ("is_enabled", "tier")
    search_fields = ("owner__username", "name", "title")
    ordering = ("owner", "order_index")
    
    list_select_related = ("owner",)
    
    inlines = [
        HeroMetricInline,
        SkillGroupInline,
        ProjectInline,
        ExperienceInline,
        ShowcaseCategoryInline,
        FeaturedModuleInline,
        LinkInline
    ]


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    """Manages messages sent via the public portfolio contact form."""
    list_display = ("display_index", "owner", "portfolio", "name", "priority", "is_dismissed", "submitted_at")
    list_filter = ("priority", "is_dismissed", "submitted_at", "owner")
    search_fields = ("owner__username", "name", "email")
    readonly_fields = ("submitted_at", "ip_address")
    ordering = ("owner", "display_index")
    
    # Prevents N+1 database queries for owner and portfolio lookups
    list_select_related = ("owner", "portfolio")


# ==========================================
# 4. BASE ADMIN FOR PORTFOLIO COMPONENTS
# ==========================================

class OrderedPortfolioModelAdmin(admin.ModelAdmin):
    """
    Abstract Base Admin to standardize the list view for models 
    that belong to a Portfolio.
    """
    list_display = ("portfolio", "get_owner", "order")
    list_filter = ("portfolio__owner",)
    search_fields = ("portfolio__name", "portfolio__owner__username")
    ordering = ("portfolio", "order")
    
    # Critical optimization: Fetches the portfolio and its owner in a single SQL query
    list_select_related = ("portfolio", "portfolio__owner")

    def get_owner(self, obj):
        return obj.portfolio.owner.username
    get_owner.short_description = 'User'

@admin.register(HeroMetric)
class HeroMetricAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "label", "value", "order")

@admin.register(SkillGroup)
class SkillGroupAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "title", "order")

@admin.register(Project)
class ProjectAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "title", "eyebrow", "order")

@admin.register(Experience)
class ExperienceAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "title", "company", "period", "order")

@admin.register(ShowcaseCategory)
class ShowcaseCategoryAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "title", "order")

@admin.register(FeaturedModule)
class FeaturedModuleAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "title", "order")

@admin.register(Link)
class LinkAdmin(OrderedPortfolioModelAdmin):
    list_display = ("portfolio", "type", "label", "order", "href")
    list_filter = ("type", "portfolio__owner")
    ordering = ("portfolio", "type", "order")