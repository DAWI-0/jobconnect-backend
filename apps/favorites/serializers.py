from rest_framework import serializers
from .models import FavoriteJob


class FavoriteJobSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    job_offer_title = serializers.CharField(source="job_offer.title", read_only=True)
    job_offer_company = serializers.CharField(source="job_offer.company.name", read_only=True)

    class Meta:
        model = FavoriteJob
        fields = [
            "id",
            "candidate", "candidate_email",
            "job_offer", "job_offer_title", "job_offer_company",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class FavoriteJobListSerializer(serializers.ModelSerializer):
    job_offer_title = serializers.CharField(source="job_offer.title", read_only=True)
    job_offer_company = serializers.CharField(source="job_offer.company.name", read_only=True)
    job_offer_location = serializers.CharField(source="job_offer.location", read_only=True)

    class Meta:
        model = FavoriteJob
        fields = [
            "id", "job_offer_title", "job_offer_company",
            "job_offer_location", "created_at",
        ]