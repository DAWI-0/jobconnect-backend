from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
)


User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):

    queryset = Conversation.objects.select_related(
        "candidate__user",
        "recruiter__user",
    ).prefetch_related(
        "messages__sender"
    ).all()

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationDetailSerializer

        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = self.queryset

        if user.role == "CANDIDATE":
            queryset = queryset.filter(
                candidate__user=user
            )

        elif user.role == "RECRUITER":
            queryset = queryset.filter(
                recruiter__user=user
            )

        elif user.role == "ADMIN":
            pass

        else:
            return queryset.none()

        # /api/conversations/?user=8
        target_user_id = self.request.query_params.get("user")

        if target_user_id:
            try:
                target_user_id = int(target_user_id)
            except ValueError:
                return queryset.none()

            queryset = queryset.filter(
                candidate__user_id=target_user_id
            ) | queryset.filter(
                recruiter__user_id=target_user_id
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        user = self.request.user
        target_user_id = serializer.validated_data.get(
            "target_user_id"
        )

        if not target_user_id:
            raise ValidationError({
                "target_user_id": "Le user ID cible est requis."
            })

        if user.id == target_user_id:
            raise ValidationError({
                "target_user_id": "Vous ne pouvez pas créer une conversation avec vous-même."
            })

        try:
            target_user = User.objects.get(
                id=target_user_id,
                is_active=True
            )
        except User.DoesNotExist:
            raise ValidationError({
                "target_user_id": "Utilisateur introuvable."
            })

        if user.role == "CANDIDATE":

            if target_user.role != "RECRUITER":
                raise ValidationError({
                    "target_user_id": "Un candidat peut contacter uniquement un recruteur."
                })

            conversation, created = Conversation.objects.get_or_create(
                candidate=user.candidate_profile,
                recruiter=target_user.recruiter_profile,
            )

        elif user.role == "RECRUITER":

            if target_user.role != "CANDIDATE":
                raise ValidationError({
                    "target_user_id": "Un recruteur peut contacter uniquement un candidat."
                })

            conversation, created = Conversation.objects.get_or_create(
                candidate=target_user.candidate_profile,
                recruiter=user.recruiter_profile,
            )

        else:
            raise ValidationError({
                "detail": "Ce rôle ne peut pas utiliser le chat."
            })

        serializer.instance = conversation


class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.select_related(
        "conversation",
        "sender",
    ).all()

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "CANDIDATE":
            return self.queryset.filter(
                conversation__candidate__user=user
            )

        if user.role == "RECRUITER":
            return self.queryset.filter(
                conversation__recruiter__user=user
            )

        if user.role == "ADMIN":
            return self.queryset

        return self.queryset.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]

        user = self.request.user

        is_participant = (
            conversation.candidate.user_id == user.id
            or conversation.recruiter.user_id == user.id
        )

        if not is_participant:
            raise ValidationError({
                "conversation": "Vous ne participez pas à cette conversation."
            })

        serializer.save(sender=user)