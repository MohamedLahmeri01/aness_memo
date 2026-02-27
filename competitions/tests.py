from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from .models import Competition


class CompetitionsTestCase(TestCase):
    """Test cases for the competitions app."""

    def setUp(self):
        self.client_api = APIClient()

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

        self.competition_data = {
            'title': 'Test Competition',
            'description': 'A test competition',
            'requirements': 'Test requirements',
            'budget': '500.00',
            'currency': 'USD',
            'deadline': (timezone.now() + timedelta(days=30)).isoformat(),
            'submission_deadline': (timezone.now() + timedelta(days=20)).isoformat(),
            'category': 'Web Development',
        }

    def test_create_competition_as_client(self):
        """Test creating a competition as a client."""
        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.post(
            '/api/competitions/create/', self.competition_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['status'], 'DRAFT')

    def test_create_competition_as_freelancer_fails(self):
        """Test that freelancers cannot create competitions."""
        self.client_api.force_authenticate(user=self.freelancer_user)
        response = self.client_api.post(
            '/api/competitions/create/', self.competition_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_status_transitions(self):
        """Test valid and invalid status transitions."""
        self.client_api.force_authenticate(user=self.client_user)

        # Create and open competition
        response = self.client_api.post(
            '/api/competitions/create/', self.competition_data, format='json'
        )
        comp_id = response.data['data']['id']

        # DRAFT -> OPEN (valid)
        response = self.client_api.post(
            f'/api/competitions/{comp_id}/status/',
            {'status': 'OPEN'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['status'], 'OPEN')

        # OPEN -> CLOSED (invalid - must go through REVIEW)
        response = self.client_api.post(
            f'/api/competitions/{comp_id}/status/',
            {'status': 'CLOSED'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # OPEN -> REVIEW (valid)
        response = self.client_api.post(
            f'/api/competitions/{comp_id}/status/',
            {'status': 'REVIEW'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ask_question_as_freelancer(self):
        """Test that freelancers can ask questions on open competitions."""
        # Create and open a competition
        competition = Competition.objects.create(
            client=self.client_user,
            title='Test',
            description='Test',
            requirements='Test',
            budget=500,
            deadline=timezone.now() + timedelta(days=30),
            submission_deadline=timezone.now() + timedelta(days=20),
            category='Test',
            status='OPEN',
        )

        self.client_api.force_authenticate(user=self.freelancer_user)
        response = self.client_api.post(
            f'/api/competitions/{competition.id}/questions/',
            {'question': 'What is the expected delivery format?'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_question_as_client(self):
        """Test that competition client can answer questions."""
        competition = Competition.objects.create(
            client=self.client_user,
            title='Test',
            description='Test',
            requirements='Test',
            budget=500,
            deadline=timezone.now() + timedelta(days=30),
            submission_deadline=timezone.now() + timedelta(days=20),
            category='Test',
            status='OPEN',
        )

        # Freelancer asks
        self.client_api.force_authenticate(user=self.freelancer_user)
        response = self.client_api.post(
            f'/api/competitions/{competition.id}/questions/',
            {'question': 'What technologies?'},
            format='json',
        )
        question_id = response.data['data']['id']

        # Client answers
        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.post(
            f'/api/competitions/{competition.id}/questions/{question_id}/answer/',
            {'answer': 'Use Django and React', 'is_public': True},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
