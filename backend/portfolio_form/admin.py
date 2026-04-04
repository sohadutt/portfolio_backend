from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ContactFormSubmission, PortfolioSettings, User, Link


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "tier",
        "enable_share_token",
        "share_token",
        "is_staff",
        "is_verified",
        "is_active",
    )
    search_fields = ("username", "email", "share_token", "is_verified")
    readonly_fields = ("share_token", "created_at")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Portfolio", {"fields": ("tier", "enable_share_token", "share_token", "created_at", "is_verified")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id","display_index","owner","name","email","for_work","submitted_at",)
    search_fields = ("owner__username","name","email","message",)
    list_filter = ("for_work", "submitted_at", "owner")
    readonly_fields = ("submitted_at", "ip_address")


@admin.register(PortfolioSettings)
class PortfolioSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "name", "title", "email")
    search_fields = ("owner__username", "owner__email", "name", "title", "email")

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "type", "label", "href")
    search_fields = ("owner__username", "owner__email", "label", "href", "value")
