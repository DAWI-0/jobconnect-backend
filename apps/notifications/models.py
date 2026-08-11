from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        APPLICATION = "APPLICATION", "Application"
        APPLICATION_STATUS = "APPLICATION_STATUS", "Application Status"
        MESSAGE = "MESSAGE", "Message"
        JOB = "JOB", "Job"
        SYSTEM = "SYSTEM", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    link = models.CharField(
        max_length=255,
        blank=True,
        help_text="Route frontend liée, ex: /applications/42",
    )

    is_read = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"