from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from apps.notifications.models import Notification


@receiver(post_save, sender=Message)
def notify_on_new_message(sender, instance, created, **kwargs):
    """Notifier le destinataire quand il reçoit un nouveau message"""
    if created:
        conversation = instance.conversation
        
        # Déterminer le destinataire (celui qui n'est PAS l'expéditeur)
        if instance.sender == conversation.candidate.user:
            recipient = conversation.recruiter.user
        else:
            recipient = conversation.candidate.user

        Notification.objects.create(
            user=recipient,
            type=Notification.NotificationType.MESSAGE,
            title="Nouveau message",
            message=f"Nouveau message de {instance.sender.get_full_name() or instance.sender.email}.",
            link=f"/conversations/{conversation.id}",
        )