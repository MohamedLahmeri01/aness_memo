from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from freelance_arena.utils import success_response
from .models import Notification
from .serializers import NotificationSerializer, MarkReadSerializer


class NotificationListView(generics.ListAPIView):
    """GET - List own notifications."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(recipient=self.request.user)
        is_read = self.request.query_params.get('is_read')
        notification_type = self.request.query_params.get('type')

        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type.upper())

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        unread_count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        return success_response(
            data={
                'notifications': response.data,
                'unread_count': unread_count,
            },
            message='Notifications retrieved.',
        )


class MarkNotificationsReadView(APIView):
    """POST - Mark specified notifications as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification_ids = serializer.validated_data['notification_ids']
        updated = Notification.objects.filter(
            id__in=notification_ids,
            recipient=request.user,
            is_read=False,
        ).update(is_read=True, read_at=timezone.now())

        return success_response(
            data={'marked_count': updated},
            message=f'{updated} notification(s) marked as read.',
        )


class MarkAllReadView(APIView):
    """POST - Mark all notifications as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).update(is_read=True, read_at=timezone.now())
        return success_response(
            data={'marked_count': updated},
            message=f'{updated} notification(s) marked as read.',
        )


class UnreadCountView(APIView):
    """GET - Get unread notification count."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = Notification.objects.filter(
            recipient=request.user, is_read=False
        ).count()
        return success_response(
            data={'unread_count': count},
            message='Unread count retrieved.',
        )
