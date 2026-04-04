import io
import secrets
import vercel_blob
from PIL import Image
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html

from .models import ContactFormSubmission, PortfolioSettings, User, Link

# --- 1. IMAGE PROCESSING UTILITY ---

def get_compressed_webp_buffer(uploaded_file, quality=80):
    """
    Converts any uploaded image to a compressed WebP byte stream.
    """
    img = Image.open(uploaded_file)
    
    # Convert to RGB (required for standard WebP conversion from PNG/RGBA)
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    buffer = io.BytesIO()
    # method=6 is the slowest/highest effort compression for smallest file size
    img.save(buffer, format="WEBP", quality=quality, method=6)
    buffer.seek(0)
    
    return buffer

# --- 2. CUSTOM USER FORM ---

class UserAdminForm(forms.ModelForm):
    """
    Adds a file upload field to the User Admin that isn't bound to the DB.
    """
    upload_profile_picture = forms.ImageField(
        required=False, 
        help_text="Upload a new photo. Old photos will be automatically deleted from Vercel."
    )

    class Meta:
        model = User
        fields = '__all__'

# --- 3. ADMIN MODEL CLASSES ---

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserAdminForm
    
    list_display = (
        "id", "username", "email", "tier", 
        "is_verified", "profile_preview", "is_staff"
    )
    
    readonly_fields = ("share_token", "created_at", "profile_preview")
    
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Portfolio & Identity", {
            "fields": (
                "tier", 
                "is_verified", 
                "upload_profile_picture",
                "profile_picture_url",     
                "profile_preview", 
                "enable_share_token", 
                "share_token", 
                "created_at"
            )
        }),
    )

    def profile_preview(self, obj):
        """Displays the circular avatar in the admin interface."""
        if obj.profile_picture_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; '
                'object-fit: cover; border: 1px solid #ccc;" />',
                obj.profile_picture_url
            )
        return "No Image"
    profile_preview.short_description = "Avatar Preview"

    def save_model(self, request, obj, form, change):
        """
        Handles the WebP conversion, Vercel Upload, and Cleanup of old images.
        """
        upload_file = form.cleaned_data.get("upload_profile_picture")
        
        if upload_file:
            # Step 1: Capture the old URL for deletion before we overwrite it
            old_url = None
            if change: # 'change' is True if we are updating an existing record
                try:
                    old_url = User.objects.get(pk=obj.pk).profile_picture_url
                except User.DoesNotExist:
                    pass

            try:
                # Step 2: Compress to WebP
                webp_buffer = get_compressed_webp_buffer(upload_file)
                
                # Step 3: Generate clean filename
                random_suffix = secrets.token_hex(3)
                filename = f"u{obj.username}_{random_suffix}.webp"
                
                # Step 4: Upload to Vercel Blob
                blob_resp = vercel_blob.put(
                    path=f"profile_pics/{filename}",
                    data=webp_buffer.read(),
                    options={
                        "access": "public",
                        "content_type": "image/webp"
                    }
                )
                
                # Step 5: Update the model field
                obj.profile_picture_url = blob_resp["url"]
                
                # Step 6: Delete the old image from the cloud
                if old_url:
                    try:
                        vercel_blob.delete(old_url)
                    except Exception:
                        # We don't crash if deletion fails (file might already be gone)
                        self.message_user(request, "New photo saved, but old file cleanup failed.", level="WARNING")

            except Exception as e:
                self.message_user(request, f"Image Upload Failed: {str(e)}", level="ERROR")
        
        super().save_model(request, obj, form, change)


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("display_index", "owner", "name", "email", "priority", "submitted_at")
    list_filter = ("priority", "submitted_at", "owner")
    search_fields = ("owner__username", "name", "email")
    readonly_fields = ("submitted_at", "ip_address")
    ordering = ("owner", "display_index")


@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(admin.ModelAdmin):
    list_display = ("owner", "name", "title", "email")
    search_fields = ("owner__username", "name", "title")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("owner", "type", "label", "order", "href")
    list_filter = ("type", "owner")
    search_fields = ("label", "href")
    ordering = ("owner", "type", "order")