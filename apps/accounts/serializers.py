from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
            raise serializers.ValidationError(
                "Must include 'email' and 'password'."
            )

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

    profile_picture = serializers.SerializerMethodField()

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
            "profile_picture",
        ]

        read_only_fields = [
            "id",
            "date_joined",
        ]

    def get_profile_picture(self, obj):

        # Candidate
        try:
            profile = obj.candidate_profile

            if profile.profile_picture:
                return profile.profile_picture.url

        except CandidateProfile.DoesNotExist:
            pass

        # Recruiter
        try:
            profile = obj.recruiter_profile

            if profile.profile_picture:
                return profile.profile_picture.url

        except RecruiterProfile.DoesNotExist:
            pass

        return None


# ============================================================
# USER CREATE
# ============================================================

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    company_name = serializers.CharField(
        write_only=True,
        required=False,
    )

    company_description = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
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
            "company_name",
            "company_description",
        ]

        read_only_fields = [
            "id",
            "username",
        ]

    def create(self, validated_data):

        from django.db import transaction
        from apps.companies.models import Company

        company_name = validated_data.pop(
            "company_name",
            "",
        )

        company_description = validated_data.pop(
            "company_description",
            "",
        )

        email = validated_data["email"]

        base = email.split("@")[0]

        username = base
        counter = 1

        while User.objects.filter(
            username=username
        ).exists():

            username = f"{base}{counter}"
            counter += 1

        validated_data["username"] = username

        with transaction.atomic():

            user = User.objects.create_user(
                **validated_data
            )

            # ================================================
            # CANDIDATE
            # ================================================

            if user.role == User.Role.CANDIDATE:

                CandidateProfile.objects.get_or_create(
                    user=user
                )

            # ================================================
            # RECRUITER
            # ================================================

            elif user.role == User.Role.RECRUITER:

                if not company_name:
                    raise serializers.ValidationError({
                        "company_name":
                        "Le nom de l'entreprise est obligatoire pour un recruteur."
                    })

                company = Company.objects.create(
                    name=company_name,
                    description=company_description,
                    owner=user,
                )

                RecruiterProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        "company": company,
                    },
                )

            return user


# ============================================================
# CANDIDATE PROFILE
# ============================================================

class CandidateProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        read_only=True
    )

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
        read_only=True,
    )

    user_first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    user_last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
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
            "bio",
            "linkedin_url",
            "github_url",
            "profile_picture",
        ]


# ============================================================
# RECRUITER PROFILE
# ============================================================

class RecruiterProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(
        read_only=True
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    class Meta:
        model = RecruiterProfile

        fields = [
            "id",
            "user",
            "company",
            "company_name",
            "profile_picture",
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
        read_only=True,
    )

    user_first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )

    user_last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )

    company_name = serializers.CharField(
        source="company.name",
        read_only=True,
    )

    class Meta:
        model = RecruiterProfile

        fields = [
            "id",
            "user_email",
            "user_first_name",
            "user_last_name",
            "company_name",
            "profile_picture",
            "phone",
            "job_title",
        ]