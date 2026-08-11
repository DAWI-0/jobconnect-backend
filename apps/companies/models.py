from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="companies/logos/",
        blank=True,
        null=True,
    )

    website = models.URLField(blank=True,null=True,)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=30, blank=True)

    location = models.CharField(max_length=255, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_companies",
    )

    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def clean(self):
        if self.owner and self.owner.role != get_user_model().Role.RECRUITER:
            raise ValidationError(
                "Le propriétaire d'une entreprise doit avoir le rôle RECRUITER."
            )

    def __str__(self):
        return self.name