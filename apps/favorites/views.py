from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FavoriteJob
from .serializers import FavoriteJobSerializer, FavoriteJobListSerializer
from apps.accounts.permissions import IsCandidate


class FavoriteJobViewSet(viewsets.ModelViewSet):
    queryset = FavoriteJob.objects.select_related("candidate", "job_offer", "job_offer__company").all()

    def get_serializer_class(self):
        if self.action == "list":
            return FavoriteJobListSerializer
        return FavoriteJobSerializer

    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return self.queryset.filter(candidate__user=self.request.user)

    def perform_create(self, serializer):
        candidate = self.request.user.candidate_profile
        serializer.save(candidate=candidate)

    @action(detail=False, methods=["post"])
    def toggle(self, request):
        job_offer_id = request.data.get("job_offer")
        candidate = request.user.candidate_profile

        favorite, created = FavoriteJob.objects.get_or_create(
            candidate=candidate,
            job_offer_id=job_offer_id,
        )

        if not created:
            favorite.delete()
            return Response({"detail": "Retiré des favoris.", "favorited": False})

        return Response({"detail": "Ajouté aux favoris.", "favorited": True})