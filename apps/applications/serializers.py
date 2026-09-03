from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["id", "candidate", "applied_at", "updated_at"]


class ApplicationListSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job_offer.title",
        read_only=True
    )
    company_name = serializers.CharField(
        source="job_offer.company.name",
        read_only=True
    )
    location = serializers.CharField(
        source="job_offer.location",
        read_only=True
    )
    contract_type = serializers.CharField(
        source="job_offer.contract_type",
        read_only=True
    )
    job_offer = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "job_offer",
            "job_title",
            "company_name",
            "location",
            "contract_type",
            "status",
            "applied_at",
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "recruiter_note"]