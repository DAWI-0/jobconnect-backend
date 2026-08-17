from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import CandidateProfile, RecruiterProfile
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    CandidateProfileSerializer,
    CandidateProfileListSerializer,
    RecruiterProfileSerializer,
    RecruiterProfileListSerializer,
)
from .permissions import IsCandidate, IsRecruiter

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CandidateProfileViewSet(viewsets.ModelViewSet):
    queryset = CandidateProfile.objects.select_related("user").all()

    def get_serializer_class(self):
        if self.action in ["list"]:
            return CandidateProfileListSerializer
        return CandidateProfileSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsCandidate()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecruiterProfileViewSet(viewsets.ModelViewSet):
    queryset = RecruiterProfile.objects.select_related("user", "company").all()

    def get_serializer_class(self):
        if self.action == "list":
            return RecruiterProfileListSerializer
        return RecruiterProfileSerializer

    def get_permissions(self):
        return [IsAuthenticated(), IsRecruiter()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)