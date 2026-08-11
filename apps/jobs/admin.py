from django.contrib import admin
from .models import Skill, JobOffer


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "recruiter",
        "contract_type",
        "experience_level",
        "status",
        "published_at",
        "created_at",
    )
    list_filter = ("status", "contract_type", "experience_level", "remote", "created_at")
    search_fields = ("title", "company__name", "description")
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("company", "recruiter", "skills")
    filter_horizontal = ("skills",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("Informations générales", {
            "fields": ("title", "company", "recruiter", "description", "location")
        }),
        ("Détails du poste", {
            "fields": ("contract_type", "experience_level", "salary_min", "salary_max", "remote", "skills")
        }),
        ("Statut & Dates", {
            "fields": ("status", "published_at", "deadline", "created_at", "updated_at")
        }),
    )