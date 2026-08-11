from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CandidateProfile, RecruiterProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_staff", "is_active", "date_joined")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role",)}),
    )


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "location", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__email", "user__username", "location")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "job_title", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__email", "user__username", "job_title", "company__name")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "company")