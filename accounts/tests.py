from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class AccountsTestCase(TestCase):
    """Test cases for the accounts app."""

    def setUp(self):
        self.client_api = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.profile_url = '/api/auth/profile/'
        self.change_password_url = '/api/auth/change-password/'

        # Create test users
        self.client_user = User.objects.create_user(
            email='client@test.com',
            username='testclient',
            password='testpass123',
            first_name='Test',
            last_name='Client',
            role='CLIENT',
        )
        self.freelancer_user = User.objects.create_user(
            email='freelancer@test.com',
            username='testfreelancer',
            password='testpass123',
            first_name='Test',
            last_name='Freelancer',
            role='FREELANCER',
        )
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='testadmin',
            password='testpass123',
            first_name='Test',
            last_name='Admin',
            role='ADMIN',
            is_staff=True,
        )

    def test_register_valid_data(self):
        """Test registration with valid data."""
        data = {
            'email': 'newuser@test.com',
            'username': 'newuser',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'CLIENT',
        }
        response = self.client_api.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails."""
        data = {
            'email': 'client@test.com',
            'username': 'anotheruser',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'first_name': 'Another',
            'last_name': 'User',
            'role': 'CLIENT',
        }
        response = self.client_api.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        data = {
            'email': 'client@test.com',
            'password': 'testpass123',
        }
        response = self.client_api.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials fails."""
        data = {
            'email': 'client@test.com',
            'password': 'wrongpassword',
        }
        response = self.client_api.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_update(self):
        """Test profile update for authenticated user."""
        self.client_api.force_authenticate(user=self.client_user)
        data = {'first_name': 'Updated', 'last_name': 'Name'}
        response = self.client_api.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['first_name'], 'Updated')

    def test_role_based_access_admin_only(self):
        """Test that non-admin users cannot access admin endpoints."""
        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        """Test that admin can list users."""
        self.client_api.force_authenticate(user=self.admin_user)
        response = self.client_api.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        """Test password change."""
        self.client_api.force_authenticate(user=self.client_user)
        data = {
            'old_password': 'testpass123',
            'new_password': 'newpass456',
            'confirm_password': 'newpass456',
        }
        response = self.client_api.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new password works
        self.client_user.refresh_from_db()
        self.assertTrue(self.client_user.check_password('newpass456'))
