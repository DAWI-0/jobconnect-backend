from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Skill, JobOffer
from .serializers import SkillSerializer, JobOfferSerializer, JobOfferListSerializer
from apps.accounts.permissions import IsRecruiter
from rest_framework.response import Response


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]


class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.select_related("company", "recruiter").prefetch_related("skills").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["contract_type", "experience_level", "remote", "status", "company"]
    search_fields = ["title", "description", "location"]
    ordering_fields = ["created_at", "salary_min", "salary_max", "published_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return JobOfferListSerializer
        return JobOfferSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated(), IsRecruiter()]

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_authenticated or self.request.user.role == "CANDIDATE":
            queryset = queryset.filter(status="PUBLISHED")
        return queryset

    def perform_create(self, serializer):
        recruiter = self.request.user.recruiter_profile
        serializer.save(recruiter=recruiter)

    @action(detail=True, methods=["post"], permission_classes=[IsRecruiter])
    def publish(self, request, pk=None):
        job_offer = self.get_object()
        job_offer.status = JobOffer.Status.PUBLISHED
        job_offer.save()
        return Response({"detail": "Offre publiée avec succès."})

    @action(detail=True, methods=["post"], permission_classes=[IsRecruiter])
    def close(self, request, pk=None):
        job_offer = self.get_object()
        job_offer.status = JobOffer.Status.CLOSED
        job_offer.save()
        return Response({"detail": "Offre fermée."})