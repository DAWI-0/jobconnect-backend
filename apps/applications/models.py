from django.core.validators import FileExtensionValidator
from django.db import models


class Application(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        REVIEWING = "REVIEWING", "Reviewing"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        INTERVIEW = "INTERVIEW", "Interview"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    job_offer = models.ForeignKey(
        "jobs.JobOffer",
        on_delete=models.PROTECT,
        related_name="applications",
    )

    candidate = models.ForeignKey(
        "accounts.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="applications",
    )

    cv = models.FileField(
        upload_to="applications/cvs/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
    )

    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )

    recruiter_note = models.TextField(blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["job_offer", "candidate"],
                name="unique_candidate_job_application",
            )
        ]

    def __str__(self):
        return (
            f"{self.candidate.user.email} - "
            f"{self.job_offer.title}"
        )