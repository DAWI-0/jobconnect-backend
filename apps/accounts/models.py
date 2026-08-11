from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CANDIDATE = "CANDIDATE", "Candidate"
        RECRUITER = "RECRUITER", "Recruiter"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CANDIDATE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class CandidateProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )

    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    cv = models.FileField(
        upload_to="cvs/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "doc", "docx"]
            )
        ],
    )

    profile_picture = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True,
    )

    linkedin_url = models.URLField(blank=True,
                                   null=True,)
    github_url = models.URLField(blank=True,
                                 null=True,)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user.role != User.Role.CANDIDATE:
            raise ValidationError(
                "Ce profil doit être associé à un utilisateur avec le rôle CANDIDATE."
            )

    def __str__(self):
        return f"Candidate: {self.user.email}"


class RecruiterProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recruiters",
    )

    phone = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user.role != User.Role.RECRUITER:
            raise ValidationError(
                "Ce profil doit être associé à un utilisateur avec le rôle RECRUITER."
            )

    def __str__(self):
        return f"Recruiter: {self.user.email}"