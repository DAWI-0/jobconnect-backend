from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()

# Test chaque import individuellement
try:
    from apps.accounts.views import UserViewSet, CandidateProfileViewSet, RecruiterProfileViewSet
    router.register(r"users", UserViewSet, basename="user")
    router.register(r"candidates", CandidateProfileViewSet, basename="candidate")
    router.register(r"recruiters", RecruiterProfileViewSet, basename="recruiter")
    print("✅ accounts views loaded")
except Exception as e:
    print(f"❌ accounts error: {e}")

try:
    from apps.companies.views import CompanyViewSet
    router.register(r"companies", CompanyViewSet, basename="company")
    print("✅ companies views loaded")
except Exception as e:
    print(f"❌ companies error: {e}")

try:
    from apps.jobs.views import SkillViewSet, JobOfferViewSet
    router.register(r"skills", SkillViewSet, basename="skill")
    router.register(r"jobs", JobOfferViewSet, basename="job")
    print("✅ jobs views loaded")
except Exception as e:
    print(f"❌ jobs error: {e}")

try:
    from apps.applications.views import ApplicationViewSet
    router.register(r"applications", ApplicationViewSet, basename="application")
    print("✅ applications views loaded")
except Exception as e:
    print(f"❌ applications error: {e}")

try:
    from apps.favorites.views import FavoriteJobViewSet
    router.register(r"favorites", FavoriteJobViewSet, basename="favorite")
    print("✅ favorites views loaded")
except Exception as e:
    print(f"❌ favorites error: {e}")

try:
    from apps.messaging.views import ConversationViewSet, MessageViewSet
    router.register(r"conversations", ConversationViewSet, basename="conversation")
    router.register(r"messages", MessageViewSet, basename="message")
    print("✅ messaging views loaded")
except Exception as e:
    print(f"❌ messaging error: {e}")

try:
    from apps.notifications.views import NotificationViewSet
    router.register(r"notifications", NotificationViewSet, basename="notification")
    print("✅ notifications views loaded")
except Exception as e:
    print(f"❌ notifications error: {e}")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)