from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()

try:
    from apps.companies.views import CompanyViewSet
    router.register(r"companies", CompanyViewSet, basename="company")
except Exception:
    pass

try:
    from apps.jobs.views import SkillViewSet, JobOfferViewSet
    router.register(r"skills", SkillViewSet, basename="skill")
    router.register(r"jobs", JobOfferViewSet, basename="job")
except Exception:
    pass

try:
    from apps.applications.views import ApplicationViewSet
    router.register(r"applications", ApplicationViewSet, basename="application")
except Exception:
    pass

try:
    from apps.favorites.views import FavoriteJobViewSet
    router.register(r"favorites", FavoriteJobViewSet, basename="favorite")
except Exception:
    pass

try:
    from apps.messaging.views import ConversationViewSet, MessageViewSet
    router.register(r"conversations", ConversationViewSet, basename="conversation")
    router.register(r"messages", MessageViewSet, basename="message")
except Exception:
    pass

try:
    from apps.notifications.views import NotificationViewSet
    router.register(r"notifications", NotificationViewSet, basename="notification")
except Exception:
    pass

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)