from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from .models import Notification


class NotificationsTestCase(TestCase):
    """Test cases for the notifications app."""

    def setUp(self):
        self.client_api = APIClient()
        self.user = User.objects.create_user(
            email='user@test.com',
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='CLIENT',
        )

        # Create test notifications
        for i in range(5):
            Notification.objects.create(
                recipient=self.user,
                notification_type='PROPOSAL_RECEIVED',
                title=f'Test Notification {i}',
                message=f'Test message {i}',
            )

    def test_list_notifications(self):
        """Test listing own notifications."""
        self.client_api.force_authenticate(user=self.user)
        response = self.client_api.get('/api/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['unread_count'], 5)

    def test_mark_all_read(self):
        """Test marking all notifications as read."""
        self.client_api.force_authenticate(user=self.user)
        response = self.client_api.post('/api/notifications/mark-all-read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify all are read
        self.assertEqual(
            Notification.objects.filter(recipient=self.user, is_read=False).count(), 0
        )
