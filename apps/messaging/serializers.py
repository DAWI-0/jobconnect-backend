from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(
        source="sender.email",
        read_only=True
    )

    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_email",
            "sender_name",
            "content",
            "is_read",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "sender",
            "created_at",
        ]

    def get_sender_name(self, obj):
        name = obj.sender.get_full_name().strip()
        return name or obj.sender.email


class ConversationSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(
        source="candidate.user.email",
        read_only=True
    )

    candidate_name = serializers.SerializerMethodField()

    candidate_user_id = serializers.IntegerField(
        source="candidate.user.id",
        read_only=True
    )

    recruiter_email = serializers.EmailField(
        source="recruiter.user.email",
        read_only=True
    )

    recruiter_name = serializers.SerializerMethodField()

    recruiter_user_id = serializers.IntegerField(
        source="recruiter.user.id",
        read_only=True
    )

    target_user_id = serializers.IntegerField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Conversation

        fields = [
            "id",

            # Candidate
            "candidate",
            "candidate_user_id",
            "candidate_email",
            "candidate_name",

            # Recruiter
            "recruiter",
            "recruiter_user_id",
            "recruiter_email",
            "recruiter_name",

            # Creation
            "target_user_id",

            # Dates
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "candidate",
            "candidate_user_id",
            "recruiter",
            "recruiter_user_id",
            "created_at",
            "updated_at",
        ]

    def get_candidate_name(self, obj):
        user = obj.candidate.user

        return (
            user.get_full_name().strip()
            or user.email
        )

    def get_recruiter_name(self, obj):
        user = obj.recruiter.user

        return (
            user.get_full_name().strip()
            or user.email
        )


class ConversationDetailSerializer(ConversationSerializer):
    messages = MessageSerializer(
        many=True,
        read_only=True
    )

    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + [
            "messages",
        ]