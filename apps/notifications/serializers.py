from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id", "user", "user_email",
            "type", "title", "message", "link",
            "is_read", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class NotificationListSerializer(serializers.ModelSerializer):
    """Version allégée"""
    class Meta:
        model = Notification
        fields = ["id", "type", "title", "is_read", "created_at"]


class MarkAsReadSerializer(serializers.ModelSerializer):
    """Pour marquer une notification comme lue"""
    class Meta:
        model = Notification
        fields = ["is_read"]