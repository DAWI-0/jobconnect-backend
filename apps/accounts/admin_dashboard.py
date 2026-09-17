from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from apps.companies.models import Company
from apps.jobs.models import JobOffer
from apps.applications.models import Application


User = get_user_model()


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if getattr(request.user, "role", None) != User.Role.ADMIN:
            return Response(
                {"detail": "Accès réservé aux administrateurs."},
                status=403,
            )

        total_users = User.objects.count()

        total_candidates = User.objects.filter(
            role=User.Role.CANDIDATE
        ).count()

        total_recruiters = User.objects.filter(
            role=User.Role.RECRUITER
        ).count()

        total_admins = User.objects.filter(
            role=User.Role.ADMIN
        ).count()

        total_companies = Company.objects.count()
        total_jobs = JobOffer.objects.count()

        total_applications = Application.objects.count()

        pending_applications = Application.objects.filter(
            status=Application.Status.PENDING
        ).count()

        accepted_applications = Application.objects.filter(
            status=Application.Status.ACCEPTED
        ).count()

        rejected_applications = Application.objects.filter(
            status=Application.Status.REJECTED
        ).count()

        return Response({
            "users": total_users,
            "candidates": total_candidates,
            "recruiters": total_recruiters,
            "admins": total_admins,
            "companies": total_companies,
            "jobs": total_jobs,
            "applications": total_applications,
            "pending_applications": pending_applications,
            "accepted_applications": accepted_applications,
            "rejected_applications": rejected_applications,
        })