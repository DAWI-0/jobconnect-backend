from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationListSerializer,
    ApplicationStatusUpdateSerializer,
)
from apps.accounts.permissions import IsCandidate, IsRecruiter


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related(
        "job_offer", "job_offer__company", "candidate", "candidate__user"
    ).all()

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationListSerializer
        if self.action in ["update", "partial_update"]:
            user = getattr(self.request, 'user', None)
            if user and user.is_authenticated and getattr(user, 'role', None) == "RECRUITER":
                return ApplicationStatusUpdateSerializer
        return ApplicationSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsCandidate()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsRecruiter()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return self.queryset
        if user.role == "CANDIDATE":
            return self.queryset.filter(candidate__user=user)
        if user.role == "RECRUITER":
            return self.queryset.filter(job_offer__recruiter__user=user)
        return self.queryset.none()

    def perform_create(self, serializer):
        candidate = self.request.user.candidate_profile
        serializer.save(candidate=candidate)

    @action(detail=True, methods=["post"], permission_classes=[IsRecruiter])
    def update_status(self, request, pk=None):
        application = self.get_object()
        serializer = ApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)