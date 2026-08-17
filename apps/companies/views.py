from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Company
from .serializers import CompanySerializer, CompanyListSerializer
from apps.accounts.permissions import IsRecruiter


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.select_related("owner").all()

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsRecruiter()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)