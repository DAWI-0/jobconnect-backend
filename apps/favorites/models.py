from django.db import models


class FavoriteJob(models.Model):
    candidate = models.ForeignKey(
        "accounts.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="favorite_jobs",
    )

    job_offer = models.ForeignKey(
        "jobs.JobOffer",
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "job_offer"],
                name="unique_candidate_favorite_job",
            )
        ]

    def __str__(self):
        return (
            f"{self.candidate.user.email} - "
            f"{self.job_offer.title}"
        )