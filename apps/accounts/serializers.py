from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, CandidateProfile, RecruiterProfile


# =========================================================
# AUTHENTICATION
# =========================================================

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
        }

        return data


# =========================================================
# USER
# =========================================================

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "role",
            "profile_picture",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "profile_picture",
        ]

    def get_profile_picture(self, obj):
        try:
            if obj.role == User.Role.CANDIDATE:
                profile = obj.candidate_profile
                if profile.profile_picture:
                    request = self.context.get("request")
                    if request:
                        return request.build_absolute_uri(
                            profile.profile_picture.url
                        )
                    return profile.profile_picture.url

            elif obj.role == User.Role.RECRUITER:
                profile = obj.recruiter_profile
                if profile.profile_picture:
                    request = self.context.get("request")
                    if request:
                        return request.build_absolute_uri(
                            profile.profile_picture.url
                        )
                    return profile.profile_picture.url

        except Exception:
            pass

        return None


# =========================================================
# CREATE USER
# =========================================================

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


# =========================================================
# CANDIDATE PROFILE
# =========================================================

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


# =========================================================
# CANDIDATE PROFILE - LIST
# =========================================================

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
            "bio",
            "linkedin_url",
            "github_url",
            "profile_picture",
            "cv",
        ]


# =========================================================
# RECRUITER PROFILE
# =========================================================

class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RecruiterProfile

        fields = [
            "id",
            "user",
            "company",
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


# =========================================================
# RECRUITER PROFILE - LIST
# =========================================================

class RecruiterProfileListSerializer(serializers.ModelSerializer):
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
        model = RecruiterProfile

        fields = [
            "id",
            "user_email",
            "user_first_name",
            "user_last_name",
            "company",
            "profile_picture",
            "phone",
            "job_title",
        ]