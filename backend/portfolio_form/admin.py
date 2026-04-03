from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ContactFormSubmission, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "username", "email", "share_token", "is_staff", "is_active")
    search_fields = ("username", "email", "share_token")
    readonly_fields = ("share_token", "created_at")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Portfolio", {"fields": ("share_token", "created_at")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id","display_index","owner","name","email","for_work","submitted_at",)
    search_fields = ("owner__username","name","email","message",)
    list_filter = ("for_work", "submitted_at", "owner")
    readonly_fields = ("submitted_at", "ip_address")
