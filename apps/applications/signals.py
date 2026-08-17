from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application
from apps.notifications.models import Notification


@receiver(post_save, sender=Application)
def notify_on_application(sender, instance, created, **kwargs):
    """Notifier le recruteur quand un candidat postule"""
    if created:
        # Notification au recruteur
        if instance.job_offer.recruiter:
            Notification.objects.create(
                user=instance.job_offer.recruiter.user,
                type=Notification.NotificationType.APPLICATION,
                title="Nouvelle candidature",
                message=f"{instance.candidate.user.get_full_name() or instance.candidate.user.email} a postulé à '{instance.job_offer.title}'.",
                link=f"/applications/{instance.id}",
            )

        # Notification au candidat (confirmation)
        Notification.objects.create(
            user=instance.candidate.user,
            type=Notification.NotificationType.APPLICATION,
            title="Candidature envoyée",
            message=f"Votre candidature pour '{instance.job_offer.title}' a été envoyée.",
            link=f"/applications/{instance.id}",
        )


@receiver(post_save, sender=Application)
def notify_on_status_change(sender, instance, created, **kwargs):
    """Notifier le candidat quand le statut de sa candidature change"""
    if not created:
        # Vérifier si le statut a changé (via update_fields ou comparaison)
        # Note: pour une vraie détection, il faudrait un signal pre_save
        # Ici on notifie à chaque save après création
        status_labels = dict(Application.Status.choices)
        Notification.objects.create(
            user=instance.candidate.user,
            type=Notification.NotificationType.APPLICATION_STATUS,
            title="Statut mis à jour",
            message=f"Votre candidature pour '{instance.job_offer.title}' est maintenant : {status_labels.get(instance.status, instance.status)}.",
            link=f"/applications/{instance.id}",
        )