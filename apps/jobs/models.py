from django.core.exceptions import ValidationError
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class JobOffer(models.Model):

    class ContractType(models.TextChoices):
        CDI = "CDI", "CDI"
        CDD = "CDD", "CDD"
        INTERNSHIP = "INTERNSHIP", "Internship"
        FREELANCE = "FREELANCE", "Freelance"
        PART_TIME = "PART_TIME", "Part Time"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "ENTRY", "Entry Level"
        JUNIOR = "JUNIOR", "Junior"
        MID = "MID", "Mid Level"
        SENIOR = "SENIOR", "Senior"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CLOSED = "CLOSED", "Closed"

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.PROTECT,
        related_name="job_offers",
    )

    recruiter = models.ForeignKey(
        "accounts.RecruiterProfile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="job_offers",
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    location = models.CharField(max_length=255, blank=True)

    contract_type = models.CharField(
        max_length=30,
        choices=ContractType.choices,
        blank=True,
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        blank=True,
    )

    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    remote = models.BooleanField(default=False)

    skills = models.ManyToManyField(
        Skill,
        related_name="job_offers",
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    deadline = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(salary_min__isnull=True)
                    | models.Q(salary_max__isnull=True)
                    | models.Q(salary_max__gte=models.F("salary_min"))
                ),
                name="salary_max_gte_salary_min",
            )
        ]

    def clean(self):
        if self.status == self.Status.PUBLISHED:
            missing = []
            if not self.description:
                missing.append("description")
            if not self.contract_type:
                missing.append("contract_type")
            if not self.experience_level:
                missing.append("experience_level")
            if missing:
                raise ValidationError(
                    f"Champs requis pour publier une offre : {', '.join(missing)}."
                )

    def __str__(self):
        return self.title