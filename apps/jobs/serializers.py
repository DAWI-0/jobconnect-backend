from rest_framework import serializers
from .models import Skill, JobOffer


# ============================================================
# SKILL
# ============================================================

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


# ============================================================
# JOB OFFER
# ============================================================

from django.utils import timezone
from rest_framework import serializers

from .models import Skill, JobOffer


# ============================================================
# SKILL
# ============================================================

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


# ============================================================
# JOB OFFER
# ============================================================

class JobOfferSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    recruiter_email = serializers.EmailField(
        source="recruiter.user.email",
        read_only=True
    )

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        source="skills",
        write_only=True,
        required=False,
    )

    class Meta:
        model = JobOffer

        fields = [
            "id",

            # Relations
            "company",
            "company_name",
            "recruiter",
            "recruiter_email",

            # Informations
            "title",
            "description",
            "location",

            # Contrat
            "contract_type",
            "experience_level",

            # Salaire
            "salary_min",
            "salary_max",

            # Options
            "remote",

            # Skills
            "skills",
            "skill_ids",

            # Status
            "status",
            "published_at",
            "deadline",

            # Dates
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "company_name",
            "recruiter_email",
            "skills",
            "published_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Création d'une offre.

        Si l'offre est créée directement avec le status PUBLISHED,
        published_at est automatiquement défini.
        """

        if validated_data.get("status") == JobOffer.Status.PUBLISHED:
            validated_data["published_at"] = timezone.now()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Mise à jour d'une offre.

        - DRAFT -> PUBLISHED :
          published_at = maintenant

        - PUBLISHED -> DRAFT :
          published_at = None

        - PUBLISHED -> PUBLISHED :
          on conserve la date originale.
        """

        new_status = validated_data.get(
            "status",
            instance.status
        )

        if (
            new_status == JobOffer.Status.PUBLISHED
            and instance.status != JobOffer.Status.PUBLISHED
        ):
            validated_data["published_at"] = timezone.now()

        elif new_status != JobOffer.Status.PUBLISHED:
            validated_data["published_at"] = None

        return super().update(
            instance,
            validated_data
        )


# ============================================================
# JOB OFFER LIST
# ============================================================

class JobOfferListSerializer(serializers.ModelSerializer):
    """Version allégée pour les listes d'offres."""

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = JobOffer

        fields = [
            "id",
            "title",
            "company_name",
            "location",
            "contract_type",
            "experience_level",
            "salary_min",
            "salary_max",
            "remote",
            "skills",
            "status",
            "published_at",
            "deadline",
        ]

