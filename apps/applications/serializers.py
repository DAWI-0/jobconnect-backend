from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["id", "candidate", "applied_at", "updated_at"]  # ← candidate ajouté


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "status", "applied_at"]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status", "recruiter_note"]