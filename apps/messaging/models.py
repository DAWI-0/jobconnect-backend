from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Conversation(models.Model):
    candidate = models.ForeignKey(
        "accounts.CandidateProfile",
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    recruiter = models.ForeignKey(
        "accounts.RecruiterProfile",
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "recruiter"],
                name="unique_candidate_recruiter_conversation",
            )
        ]

    def __str__(self):
        return (
            f"{self.candidate.user.email} - "
            f"{self.recruiter.user.email}"
        )


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )

    content = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["created_at"]

    def clean(self):
        valid_sender_ids = {
            self.conversation.candidate.user_id,
            self.conversation.recruiter.user_id,
        }
        if self.sender_id not in valid_sender_ids:
            raise ValidationError(
                "L'expéditeur doit être un participant de cette conversation."
            )

    def __str__(self):
        return f"Message #{self.id}"