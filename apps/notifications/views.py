from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer, MarkAsReadSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related("user").all()

    def get_serializer_class(self):
        if self.action == "list":
            return NotificationListSerializer
        if self.action == "mark_as_read":
            return MarkAsReadSerializer
        return NotificationSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marquée comme lue."})

    @action(detail=False, methods=["post"])
    def mark_all_as_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({"detail": "Toutes les notifications marquées comme lues."})

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": count})