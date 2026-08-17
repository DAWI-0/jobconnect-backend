from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification


@receiver(post_save, sender=Notification)
def send_realtime_notification(sender, instance, created, **kwargs):
    """Envoyer la notification en temps réel via WebSocket (Channels)"""
    if created:
        # Ici tu peux intégrer Django Channels pour envoyer
        # la notification en temps réel au frontend
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.user.id}",
            {
                "type": "send_notification",
                "notification": {
                    "id": instance.id,
                    "type": instance.type,
                    "title": instance.title,
                    "message": instance.message,
                    "link": instance.link,
                    "created_at": str(instance.created_at),
                }
            }
        )