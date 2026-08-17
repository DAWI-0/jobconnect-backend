from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import JobOffer
from apps.notifications.models import Notification


@receiver(post_save, sender=JobOffer)
def notify_on_job_publish(sender, instance, created, **kwargs):
    """Notifier quand une offre est publiée"""
    if not created and instance.status == JobOffer.Status.PUBLISHED:
        # Notifier les candidats qui ont cette entreprise en favori (optionnel)
        # Ou notifier tous les candidats (à adapter selon ta logique)
        pass  # À implémenter selon tes besoins