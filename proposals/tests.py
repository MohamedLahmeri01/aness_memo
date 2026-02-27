from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from competitions.models import Competition
from .models import Proposal


class ProposalsTestCase(TestCase):
    """Test cases for the proposals app."""

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
        self.freelancer_user2 = User.objects.create_user(
            email='freelancer2@test.com',
            username='testfreelancer2',
            password='testpass123',
            first_name='Test2',
            last_name='Freelancer2',
            role='FREELANCER',
        )

        self.competition = Competition.objects.create(
            client=self.client_user,
            title='Test Competition',
            description='Test description',
            requirements='Test requirements',
            budget=1000,
            deadline=timezone.now() + timedelta(days=30),
            submission_deadline=timezone.now() + timedelta(days=20),
            category='Web Development',
            status='OPEN',
        )

        self.proposal_data = {
            'competition': str(self.competition.id),
            'title': 'My Proposal',
            'description': 'I will build this amazing thing.',
            'proposed_budget': '800.00',
            'estimated_duration': 14,
        }

    def test_submit_proposal_as_freelancer(self):
        """Test submitting a proposal as a freelancer."""
        self.client_api.force_authenticate(user=self.freelancer_user)
        response = self.client_api.post(
            '/api/proposals/submit/', self.proposal_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_proposal_fails(self):
        """Test that submitting duplicate proposal fails."""
        self.client_api.force_authenticate(user=self.freelancer_user)
        self.client_api.post('/api/proposals/submit/', self.proposal_data, format='json')

        response = self.client_api.post(
            '/api/proposals/submit/', self.proposal_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_after_deadline_fails(self):
        """Test that submitting after deadline fails."""
        self.competition.submission_deadline = timezone.now() - timedelta(days=1)
        self.competition.save()

        self.client_api.force_authenticate(user=self.freelancer_user)
        response = self.client_api.post(
            '/api/proposals/submit/', self.proposal_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blind_review_enforcement(self):
        """Test that client cannot see freelancer identity in proposal list."""
        # Create proposals from two freelancers
        Proposal.objects.create(
            competition=self.competition,
            freelancer=self.freelancer_user,
            title='Proposal 1',
            description='Description 1',
            proposed_budget=800,
            estimated_duration=10,
        )
        Proposal.objects.create(
            competition=self.competition,
            freelancer=self.freelancer_user2,
            title='Proposal 2',
            description='Description 2',
            proposed_budget=900,
            estimated_duration=12,
        )

        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.get(
            f'/api/proposals/competition/{self.competition.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify no freelancer identity is exposed
        proposals = response.data['data']
        if isinstance(proposals, dict) and 'results' in proposals:
            proposals = proposals['results']
        for proposal in proposals:
            self.assertNotIn('freelancer', proposal)
            self.assertNotIn('freelancer_username', proposal)

    def test_select_winner(self):
        """Test selecting a winner for a competition."""
        # Create a proposal
        proposal = Proposal.objects.create(
            competition=self.competition,
            freelancer=self.freelancer_user,
            title='Winning Proposal',
            description='Great work',
            proposed_budget=800,
            estimated_duration=10,
        )

        # Move to REVIEW
        self.competition.status = 'REVIEW'
        self.competition.save()

        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.post(
            f'/api/competitions/{self.competition.id}/select-winner/',
            {'proposal_id': str(proposal.id)},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify competition is closed
        self.competition.refresh_from_db()
        self.assertEqual(self.competition.status, 'CLOSED')
        self.assertEqual(self.competition.winner, self.freelancer_user)

        # Verify proposal is accepted
        proposal.refresh_from_db()
        self.assertTrue(proposal.is_winner)
        self.assertEqual(proposal.status, 'ACCEPTED')
