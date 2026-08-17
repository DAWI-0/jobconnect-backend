from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source="sender.email", read_only=True)
    sender_name = serializers.CharField(source="sender.get_full_name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "conversation", "sender", "sender_email", "sender_name",
            "content", "is_read", "created_at",
        ]
        read_only_fields = ["id", "sender", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    candidate_name = serializers.CharField(source="candidate.user.get_full_name", read_only=True)
    recruiter_email = serializers.EmailField(source="recruiter.user.email", read_only=True)
    recruiter_name = serializers.CharField(source="recruiter.user.get_full_name", read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "candidate", "candidate_email", "candidate_name",
            "recruiter", "recruiter_email", "recruiter_name",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "candidate", "created_at", "updated_at"]


class ConversationDetailSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(source="candidate.user.email", read_only=True)
    candidate_name = serializers.CharField(source="candidate.user.get_full_name", read_only=True)
    recruiter_email = serializers.EmailField(source="recruiter.user.email", read_only=True)
    recruiter_name = serializers.CharField(source="recruiter.user.get_full_name", read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "candidate", "candidate_email", "candidate_name",
            "recruiter", "recruiter_email", "recruiter_name",
            "messages",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "candidate", "created_at", "updated_at"]