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

    # --------------------------------------------------------
    # Recruiter information
    # --------------------------------------------------------

    recruiter_user_id = serializers.IntegerField(
        source="recruiter.user.id",
        read_only=True
    )

    recruiter_name = serializers.SerializerMethodField()

    recruiter_email = serializers.EmailField(
        source="recruiter.user.email",
        read_only=True
    )

    recruiter_job_title = serializers.CharField(
        source="recruiter.job_title",
        read_only=True
    )

    recruiter_phone = serializers.CharField(
        source="recruiter.phone",
        read_only=True
    )

    recruiter_profile_picture = serializers.ImageField(
        source="recruiter.profile_picture",
        read_only=True
    )

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        source="skills",
        write_only=True,
        required=False
    )

    # --------------------------------------------------------
    # Recruiter name
    # --------------------------------------------------------

    def get_recruiter_name(self, obj):

        if not obj.recruiter or not obj.recruiter.user:
            return ""

        user = obj.recruiter.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        return full_name or user.username or user.email

    # ========================================================
    # META
    # ========================================================

    class Meta:

        model = JobOffer

        fields = [
            "id",

            # Company
            "company",
            "company_name",

            # Recruiter
            "recruiter",
            "recruiter_user_id",
            "recruiter_name",
            "recruiter_email",
            "recruiter_job_title",
            "recruiter_phone",
            "recruiter_profile_picture",

            # Job
            "title",
            "description",
            "location",

            # Contract
            "contract_type",
            "experience_level",

            # Salary
            "salary_min",
            "salary_max",

            # Work mode
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

            "company",
            "company_name",

            "recruiter",
            "recruiter_user_id",
            "recruiter_name",
            "recruiter_email",
            "recruiter_job_title",
            "recruiter_phone",
            "recruiter_profile_picture",

            "skills",
            "published_at",

            "created_at",
            "updated_at",
        ]

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate(self, attrs):

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({
                "detail": "Vous devez etre authentifie."
            })

        user = request.user

        if user.role != user.Role.RECRUITER:
            raise serializers.ValidationError({
                "detail": "Seul un recruteur peut creer une offre."
            })

        # ----------------------------------------------------
        # Update ownership
        # ----------------------------------------------------

        if self.instance:

            if (
                not self.instance.recruiter
                or self.instance.recruiter.user_id != user.id
            ):
                raise serializers.ValidationError({
                    "detail": "Vous ne pouvez pas modifier cette offre."
                })

        # ----------------------------------------------------
        # Salary validation
        # ----------------------------------------------------

        salary_min = attrs.get("salary_min")
        salary_max = attrs.get("salary_max")

        if salary_min is not None and salary_max is not None:

            if salary_min > salary_max:
                raise serializers.ValidationError({
                    "salary_max":
                    "Le salaire maximum doit etre superieur au salaire minimum."
                })

        return attrs

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, validated_data):

        request = self.context["request"]
        user = request.user

        try:
            recruiter = user.recruiter_profile

        except Exception:
            raise serializers.ValidationError({
                "recruiter":
                "Votre profil recruteur n'existe pas."
            })

        if not recruiter.company:

            raise serializers.ValidationError({
                "company":
                "Aucune entreprise n'est associee a votre profil recruteur."
            })

        company = recruiter.company

        skills = validated_data.pop(
            "skills",
            []
        )

        # ----------------------------------------------------
        # Published date
        # ----------------------------------------------------

        if validated_data.get("status") == JobOffer.Status.PUBLISHED:

            validated_data["published_at"] = timezone.now()

        # ----------------------------------------------------
        # Create job
        # ----------------------------------------------------

        job = JobOffer.objects.create(
            recruiter=recruiter,
            company=company,
            **validated_data
        )

        # ----------------------------------------------------
        # Skills
        # ----------------------------------------------------

        if skills:
            job.skills.set(skills)

        return job

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, instance, validated_data):

        # Company and recruiter cannot be changed
        validated_data.pop(
            "company",
            None
        )

        validated_data.pop(
            "recruiter",
            None
        )

        skills = validated_data.pop(
            "skills",
            None
        )

        new_status = validated_data.get(
            "status",
            instance.status
        )

        # ----------------------------------------------------
        # Published
        # ----------------------------------------------------

        if (
            new_status == JobOffer.Status.PUBLISHED
            and instance.status != JobOffer.Status.PUBLISHED
        ):

            validated_data["published_at"] = timezone.now()

        # ----------------------------------------------------
        # Not published
        # ----------------------------------------------------

        elif new_status != JobOffer.Status.PUBLISHED:

            validated_data["published_at"] = None

        # ----------------------------------------------------
        # Update job
        # ----------------------------------------------------

        instance = super().update(
            instance,
            validated_data
        )

        # ----------------------------------------------------
        # Update skills
        # ----------------------------------------------------

        if skills is not None:

            instance.skills.set(skills)

        return instance


# ============================================================
# JOB OFFER LIST
# ============================================================

class JobOfferListSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    # --------------------------------------------------------
    # Recruiter information
    # --------------------------------------------------------

    recruiter_user_id = serializers.IntegerField(
        source="recruiter.user.id",
        read_only=True
    )

    recruiter_name = serializers.SerializerMethodField()

    recruiter_email = serializers.EmailField(
        source="recruiter.user.email",
        read_only=True
    )

    recruiter_job_title = serializers.CharField(
        source="recruiter.job_title",
        read_only=True
    )

    recruiter_phone = serializers.CharField(
        source="recruiter.phone",
        read_only=True
    )

    recruiter_profile_picture = serializers.ImageField(
        source="recruiter.profile_picture",
        read_only=True
    )

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    # --------------------------------------------------------
    # Recruiter name
    # --------------------------------------------------------

    def get_recruiter_name(self, obj):

        if not obj.recruiter or not obj.recruiter.user:
            return ""

        user = obj.recruiter.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        return full_name or user.username or user.email

    # ========================================================
    # META
    # ========================================================

    class Meta:

        model = JobOffer

        fields = [
            "id",
            "title",

            # Company
            "company_name",

            # Recruiter
            "recruiter_user_id",
            "recruiter_name",
            "recruiter_email",
            "recruiter_job_title",
            "recruiter_phone",
            "recruiter_profile_picture",

            # Job information
            "location",
            "contract_type",
            "experience_level",

            # Salary
            "salary_min",
            "salary_max",

            # Work mode
            "remote",

            # Skills
            "skills",

            # Status
            "status",
            "published_at",
            "deadline",
        ]