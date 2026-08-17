from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import CandidateProfile, RecruiterProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement le profil (Candidate ou Recruiter) à l'inscription"""
    if created:
        if instance.role == User.Role.CANDIDATE:
            CandidateProfile.objects.create(user=instance)
        elif instance.role == User.Role.RECRUITER:
            RecruiterProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand le User est sauvegardé"""
    if hasattr(instance, "candidate_profile"):
        instance.candidate_profile.save()
    elif hasattr(instance, "recruiter_profile"):
        instance.recruiter_profile.save()