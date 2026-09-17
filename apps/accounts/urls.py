from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    UserViewSet,
    CandidateProfileViewSet,
    RecruiterProfileViewSet,
)

from .serializers import EmailTokenObtainPairSerializer
from .admin_dashboard import AdminDashboardView


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class VerifyView(TokenVerifyView):
    permission_classes = [AllowAny]


router = DefaultRouter()

router.register(
    r"users",
    UserViewSet,
    basename="user"
)

router.register(
    r"candidates",
    CandidateProfileViewSet,
    basename="candidate"
)

router.register(
    r"recruiters",
    RecruiterProfileViewSet,
    basename="recruiter"
)


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "refresh/",
        RefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "verify/",
        VerifyView.as_view(),
        name="token_verify",
    ),

    path(
        "admin/dashboard/",
        AdminDashboardView.as_view(),
        name="admin_dashboard",
    ),
] + router.urls