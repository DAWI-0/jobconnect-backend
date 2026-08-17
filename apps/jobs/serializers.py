from rest_framework import serializers
from .models import Skill, JobOffer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class JobOfferSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    recruiter_email = serializers.EmailField(source="recruiter.user.email", read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
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
            "company", "company_name",
            "recruiter", "recruiter_email",
            "title", "description", "location",
            "contract_type", "experience_level",
            "salary_min", "salary_max", "remote",
            "skills", "skill_ids",
            "status", "published_at", "deadline",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class JobOfferListSerializer(serializers.ModelSerializer):
    """Version allégée pour les listes d'offres"""
    company_name = serializers.CharField(source="company.name", read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobOffer
        fields = [
            "id", "title", "company_name", "location",
            "contract_type", "experience_level",
            "salary_min", "salary_max", "remote",
            "skills", "status", "published_at", "deadline",
        ]