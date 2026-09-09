from django.utils import timezone
from rest_framework import serializers

from .models import Skill, JobOffer


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


class JobOfferSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    recruiter_email = serializers.EmailField(
        source="recruiter.user.email",
        read_only=True
    )

    # Skills retournes en lecture
    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    # Skills envoyes par le frontend
    skill_ids = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        source="skills",
        write_only=True,
        required=False
    )

    class Meta:
        model = JobOffer

        fields = [
            "id",

            # Company / Recruiter
            "company",
            "company_name",
            "recruiter",
            "recruiter_email",

            # Informations offre
            "title",
            "description",
            "location",

            # Contrat
            "contract_type",
            "experience_level",

            # Salaire
            "salary_min",
            "salary_max",

            # Travail
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

            # Automatiques
            "company",
            "company_name",
            "recruiter",
            "recruiter_email",

            # Automatique
            "skills",
            "published_at",

            # Dates
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        request = self.context.get("request")

        # Verifier authentification
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({
                "detail": "Vous devez etre authentifie."
            })

        user = request.user

        # Seul recruiter
        if user.role != user.Role.RECRUITER:
            raise serializers.ValidationError({
                "detail": "Seul un recruteur peut creer une offre."
            })

        # En modification, verifier que l'offre appartient au recruiter
        if self.instance:
            if self.instance.recruiter.user_id != user.id:
                raise serializers.ValidationError({
                    "detail": "Vous ne pouvez pas modifier cette offre."
                })

        # Verifier salaire
        salary_min = attrs.get("salary_min")
        salary_max = attrs.get("salary_max")

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise serializers.ValidationError({
                    "salary_max": "Le salaire maximum doit etre superieur au salaire minimum."
                })

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        # Recuperer le profil recruiter
        try:
            recruiter = user.recruiter_profile
        except Exception:
            raise serializers.ValidationError({
                "recruiter": "Votre profil recruteur n'existe pas."
            })

        # Recuperer automatiquement la company
        if not recruiter.company:
            raise serializers.ValidationError({
                "company": "Aucune entreprise n'est associee a votre profil recruteur."
            })

        company = recruiter.company

        # IMPORTANT:
        # skills est un ManyToMany.
        # On doit le retirer avant JobOffer.objects.create()
        skills = validated_data.pop("skills", [])

        # Si l'offre est publiee directement
        if validated_data.get("status") == JobOffer.Status.PUBLISHED:
            validated_data["published_at"] = timezone.now()

        # Creation de l'offre
        job = JobOffer.objects.create(
            recruiter=recruiter,
            company=company,
            **validated_data
        )

        # Ajouter les skills apres creation
        if skills:
            job.skills.set(skills)

        return job

    def update(self, instance, validated_data):
        # Impossible de modifier company/recruiter
        validated_data.pop("company", None)
        validated_data.pop("recruiter", None)

        # Recuperer les skills
        skills = validated_data.pop("skills", None)

        # Nouveau status
        new_status = validated_data.get(
            "status",
            instance.status
        )

        # Publication
        if (
            new_status == JobOffer.Status.PUBLISHED
            and instance.status != JobOffer.Status.PUBLISHED
        ):
            validated_data["published_at"] = timezone.now()

        # Si on quitte Published
        elif new_status != JobOffer.Status.PUBLISHED:
            validated_data["published_at"] = None

        # Update des champs normaux
        instance = super().update(
            instance,
            validated_data
        )

        # Update des skills
        if skills is not None:
            instance.skills.set(skills)

        return instance


class JobOfferListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    skills = SkillSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = JobOffer

        fields = [
            "id",
            "title",
            "company_name",
            "location",
            "contract_type",
            "experience_level",
            "salary_min",
            "salary_max",
            "remote",
            "skills",
            "status",
            "published_at",
            "deadline",
        ]