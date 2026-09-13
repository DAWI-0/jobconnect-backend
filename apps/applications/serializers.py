from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = [
            "id",
            "candidate",
            "applied_at",
            "updated_at",
        ]


class ApplicationListSerializer(serializers.ModelSerializer):

    # =========================
    # JOB INFORMATION
    # =========================

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

    # =========================
    # CANDIDATE INFORMATION
    # =========================

    candidate_user_id = serializers.IntegerField(
        source="candidate.user.id",
        read_only=True
    )

    candidate_name = serializers.SerializerMethodField()

    candidate_email = serializers.EmailField(
        source="candidate.user.email",
        read_only=True
    )

    candidate_phone = serializers.CharField(
        source="candidate.phone",
        read_only=True
    )

    candidate_location = serializers.CharField(
        source="candidate.location",
        read_only=True
    )

    candidate_bio = serializers.CharField(
        source="candidate.bio",
        read_only=True
    )

    candidate_linkedin = serializers.URLField(
        source="candidate.linkedin_url",
        read_only=True
    )

    candidate_github = serializers.URLField(
        source="candidate.github_url",
        read_only=True
    )

    candidate_profile_picture = serializers.ImageField(
        source="candidate.profile_picture",
        read_only=True
    )

    # =========================
    # RECRUITER INFORMATION
    # =========================

    recruiter_user_id = serializers.IntegerField(
        source="job_offer.recruiter.user.id",
        read_only=True
    )

    recruiter_name = serializers.SerializerMethodField()

    recruiter_email = serializers.EmailField(
        source="job_offer.recruiter.user.email",
        read_only=True
    )

    recruiter_job_title = serializers.CharField(
        source="job_offer.recruiter.job_title",
        read_only=True
    )

    recruiter_phone = serializers.CharField(
        source="job_offer.recruiter.phone",
        read_only=True
    )

    recruiter_profile_picture = serializers.ImageField(
        source="job_offer.recruiter.profile_picture",
        read_only=True
    )

    # =========================
    # METHODS
    # =========================

    def get_candidate_name(self, obj):
        if not obj.candidate or not obj.candidate.user:
            return ""

        user = obj.candidate.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        return full_name or user.username or user.email

    def get_recruiter_name(self, obj):
        recruiter = obj.job_offer.recruiter

        if not recruiter or not recruiter.user:
            return ""

        user = recruiter.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        return full_name or user.username or user.email

    # =========================
    # RESPONSE FIELDS
    # =========================

    class Meta:
        model = Application

        fields = [
            "id",

            # Job
            "job_offer",
            "job_title",
            "company_name",
            "location",
            "contract_type",

            # Candidate
            "candidate_user_id",
            "candidate_name",
            "candidate_email",
            "candidate_phone",
            "candidate_location",
            "candidate_bio",
            "candidate_linkedin",
            "candidate_github",
            "candidate_profile_picture",

            # Recruiter
            "recruiter_user_id",
            "recruiter_name",
            "recruiter_email",
            "recruiter_job_title",
            "recruiter_phone",
            "recruiter_profile_picture",

            # Application
            "status",
            "applied_at",
        ]


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "status",
            "recruiter_note",
        ]