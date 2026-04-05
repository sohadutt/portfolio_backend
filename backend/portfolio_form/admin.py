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

# --- 1. IMAGE PROCESSING UTILITY ---

def get_compressed_webp_buffer(uploaded_file, quality=80):
    """Converts any uploaded image to a compressed WebP byte stream."""
    img = Image.open(uploaded_file)
    if img.mode != "RGB":
        img = img.convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="WEBP", quality=quality, method=6)
    buffer.seek(0)
    return buffer

# --- 2. CUSTOM USER FORM ---

class UserAdminForm(forms.ModelForm):
    upload_profile_picture = forms.ImageField(
        required=False, 
        help_text="Upload a new photo. Old photos will be automatically deleted from Vercel."
    )

    class Meta:
        model = User
        fields = '__all__'

# --- 3. ADMIN CLASSES ---

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
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
        if obj.profile_picture_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; '
                'object-fit: cover; border: 1px solid #ccc;" />',
                obj.profile_picture_url
            )
        return "No Image"
    profile_preview.short_description = "Avatar Preview"

    def save_model(self, request, obj, form, change):
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
    list_display = ("owner", "order_index", "is_enabled", "tier", "name", "title")
    list_filter = ("is_enabled", "tier")
    search_fields = ("owner__username", "name", "title")
    ordering = ("owner", "order_index")


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    # Updated to include 'portfolio'
    list_display = ("display_index", "owner", "portfolio", "name", "priority", "is_dismissed", "submitted_at")
    list_filter = ("priority", "is_dismissed", "submitted_at", "owner")
    search_fields = ("owner__username", "name", "email")
    readonly_fields = ("submitted_at", "ip_address")
    ordering = ("owner", "display_index")


# --- Base Admin for Portfolio Components ---

class OrderedPortfolioModelAdmin(admin.ModelAdmin):
    """
    Standardizes Admin for models linked to PortfolioSettings.
    """
    list_display = ("portfolio", "get_owner", "order")
    list_filter = ("portfolio__owner",)
    search_fields = ("portfolio__name", "portfolio__owner__username")
    ordering = ("portfolio", "order")

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