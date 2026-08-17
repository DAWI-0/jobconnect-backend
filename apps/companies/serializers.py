from rest_framework import serializers
from .models import Company
from apps.accounts.models import User

class CompanySerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="owner",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Company
        fields = [
            "id", "name", "description",
            "logo", "website", "email", "phone", "location",
            "owner", "owner_email", "owner_id",
            "is_active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class CompanyListSerializer(serializers.ModelSerializer):
    """Version allégée pour les listes"""
    class Meta:
        model = Company
        fields = ["id", "name", "logo", "location", "is_active"]