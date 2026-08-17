from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Vues JWT avec permission AllowAny (sinon IsAuthenticated bloque tout)
class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

class VerifyView(TokenVerifyView):
    permission_classes = [AllowAny]

urlpatterns = [
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
    path("verify/", VerifyView.as_view(), name="token_verify"),
]