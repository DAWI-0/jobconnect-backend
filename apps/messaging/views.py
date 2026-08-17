from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.select_related(
        "candidate",
        "recruiter",
    ).all()

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationDetailSerializer

        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == "CANDIDATE":
            return self.queryset.filter(
                candidate__user=user
            )

        if user.role == "RECRUITER":
            return self.queryset.filter(
                recruiter__user=user
            )

        return self.queryset

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "CANDIDATE":
            serializer.save(
                candidate=user.candidate_profile
            )

        elif user.role == "RECRUITER":
            serializer.save(
                recruiter=user.recruiter_profile
            )


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

        return self.queryset

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)