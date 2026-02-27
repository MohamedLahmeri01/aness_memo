from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from competitions.models import Competition
from proposals.models import Proposal
from .models import Review


class FeedbackTestCase(TestCase):
    """Test cases for the feedback app."""

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

        self.competition = Competition.objects.create(
            client=self.client_user,
            title='Test Competition',
            description='Test',
            requirements='Test',
            budget=1000,
            deadline=timezone.now() + timedelta(days=30),
            submission_deadline=timezone.now() + timedelta(days=20),
            category='Test',
            status='CLOSED',
            winner=self.freelancer_user,
        )

        self.proposal = Proposal.objects.create(
            competition=self.competition,
            freelancer=self.freelancer_user,
            title='Test Proposal',
            description='Test',
            proposed_budget=800,
            estimated_duration=10,
            status='ACCEPTED',
            is_winner=True,
        )

    def test_review_after_closed_competition(self):
        """Test creating a review after competition is closed."""
        self.client_api.force_authenticate(user=self.client_user)
        data = {
            'competition': str(self.competition.id),
            'reviewee': str(self.freelancer_user.id),
            'rating': 5,
            'comment': 'Excellent work!',
        }
        response = self.client_api.post(
            '/api/feedback/reviews/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_open_competition_fails(self):
        """Test that reviews on open competitions fail."""
        self.competition.status = 'OPEN'
        self.competition.save()

        self.client_api.force_authenticate(user=self.client_user)
        data = {
            'competition': str(self.competition.id),
            'reviewee': str(self.freelancer_user.id),
            'rating': 5,
            'comment': 'Great!',
        }
        response = self.client_api.post(
            '/api/feedback/reviews/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_review_fails(self):
        """Test that duplicate reviews for the same competition fail."""
        self.client_api.force_authenticate(user=self.client_user)
        data = {
            'competition': str(self.competition.id),
            'reviewee': str(self.freelancer_user.id),
            'rating': 4,
            'comment': 'Good work.',
        }
        self.client_api.post('/api/feedback/reviews/', data, format='json')

        response = self.client_api.post(
            '/api/feedback/reviews/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
