from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "email", "location", "owner__email")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("owner",)