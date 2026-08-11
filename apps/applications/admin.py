from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job_offer", "status", "applied_at", "updated_at")
    list_filter = ("status", "applied_at", "updated_at")
    search_fields = ("candidate__user__email", "job_offer__title")
    readonly_fields = ("applied_at", "updated_at")
    autocomplete_fields = ("candidate", "job_offer")

    fieldsets = (
        ("Candidature", {
            "fields": ("job_offer", "candidate", "status")
        }),
        ("Documents", {
            "fields": ("cv", "cover_letter")
        }),
        ("Notes", {
            "fields": ("recruiter_note",)
        }),
        ("Dates", {
            "fields": ("applied_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )