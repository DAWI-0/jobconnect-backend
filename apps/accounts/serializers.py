from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from .models import CandidateProfile, RecruiterProfile

User = get_user_model()


# ============================================================
# JWT LOGIN PAR EMAIL
# ============================================================

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
            )

        attrs["username"] = user.username
        return super().validate(attrs)


# ============================================================
# USER
# ============================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "date_joined",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        read_only_fields = [
            "id",
            "username",
        ]

    def create(self, validated_data):
        email = validated_data["email"]
        base = email.split("@")[0]
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base}{counter}"
            counter += 1

        validated_data["username"] = username
        return User.objects.create_user(**validated_data)


# ============================================================
# CANDIDATE PROFILE
# ============================================================

class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            "id",
            "user",
            "phone",
            "location",
            "bio",
            "cv",
            "profile_picture",
            "linkedin_url",
            "github_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


class CandidateProfileListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    user_first_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    user_last_name = serializers.CharField(
        source="user.last_name",
        read_only=True
    )

    class Meta:
        model = CandidateProfile
        fields = [
            "id",
            "user_email",
            "user_first_name",
            "user_last_name",
            "phone",
            "location",
            "profile_picture",
        ]


# ============================================================
# RECRUITER PROFILE
# ============================================================

class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    class Meta:
        model = RecruiterProfile
        fields = [
            "id",
            "user",
            "company",
            "company_name",
            "phone",
            "job_title",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
        ]


class RecruiterProfileListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    class Meta:
        model = RecruiterProfile
        fields = [
            "id",
            "user_email",
            "company_name",
            "job_title",
        ]