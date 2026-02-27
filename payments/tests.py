from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from accounts.models import User
from competitions.models import Competition
from proposals.models import Proposal
from .models import PaymentRecord


class PaymentsTestCase(TestCase):
    """Test cases for the payments app."""

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
            budget=Decimal('500.00'),
            deadline=timezone.now() + timedelta(days=30),
            submission_deadline=timezone.now() + timedelta(days=20),
            category='Test',
            status='REVIEW',
        )

        self.proposal = Proposal.objects.create(
            competition=self.competition,
            freelancer=self.freelancer_user,
            title='Test Proposal',
            description='Test',
            proposed_budget=Decimal('400.00'),
            estimated_duration=10,
        )

    def test_payment_created_on_winner_selection(self):
        """Test that a payment record is created when a winner is selected."""
        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.post(
            f'/api/competitions/{self.competition.id}/select-winner/',
            {'proposal_id': str(self.proposal.id)},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify payment record exists
        self.assertTrue(PaymentRecord.objects.filter(competition=self.competition).exists())

    def test_platform_fee_calculation(self):
        """Test that platform fee is calculated correctly (10%)."""
        payment = PaymentRecord.objects.create(
            competition=self.competition,
            client=self.client_user,
            freelancer=self.freelancer_user,
            amount=Decimal('500.00'),
        )

        self.assertEqual(payment.platform_fee, Decimal('50.00'))
        self.assertEqual(payment.net_amount, Decimal('450.00'))

    def test_client_can_view_own_payments(self):
        """Test that clients can view their own payment records."""
        PaymentRecord.objects.create(
            competition=self.competition,
            client=self.client_user,
            freelancer=self.freelancer_user,
            amount=Decimal('500.00'),
        )

        self.client_api.force_authenticate(user=self.client_user)
        response = self.client_api.get('/api/payments/client/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
