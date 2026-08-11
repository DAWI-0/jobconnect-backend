from django.contrib import admin
from .models import FavoriteJob


@admin.register(FavoriteJob)
class FavoriteJobAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job_offer", "created_at")
    list_filter = ("created_at",)
    search_fields = ("candidate__user__email", "job_offer__title")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("candidate", "job_offer")