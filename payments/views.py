from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from freelance_arena.utils import success_response
from accounts.permissions import IsClient, IsFreelancer, IsAdminRole
from .models import PaymentRecord
from .serializers import (
    PaymentRecordSerializer,
    ClientPaymentSerializer,
    FreelancerPaymentSerializer,
    UpdatePaymentStatusSerializer,
)


class MyClientPaymentsView(generics.ListAPIView):
    """GET - Client's own payment records."""
    serializer_class = ClientPaymentSerializer
    permission_classes = [IsAuthenticated, IsClient]

    def get_queryset(self):
        return PaymentRecord.objects.filter(client=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Client payments retrieved.')


class MyFreelancerPaymentsView(generics.ListAPIView):
    """GET - Freelancer's own payment records received."""
    serializer_class = FreelancerPaymentSerializer
    permission_classes = [IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return PaymentRecord.objects.filter(freelancer=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Freelancer payments retrieved.')


class PaymentDetailView(APIView):
    """GET - Payment detail. Accessible by payment client, freelancer, or admin."""
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(PaymentRecord, id=payment_id)

        # Check permissions
        if (request.user != payment.client and
                request.user != payment.freelancer and
                request.user.role != 'ADMIN'):
            return success_response(
                data=None, message='You do not have permission to view this payment.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = PaymentRecordSerializer(payment)
        return success_response(data=serializer.data, message='Payment detail retrieved.')


class AdminPaymentListView(generics.ListAPIView):
    """GET - Admin only. All payments with filters."""
    serializer_class = PaymentRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = PaymentRecord.objects.all()
        status_filter = self.request.query_params.get('status')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='All payments retrieved.')


class UpdatePaymentStatusView(APIView):
    """POST - Admin only. Update payment status."""
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request, payment_id):
        payment = get_object_or_404(PaymentRecord, id=payment_id)

        serializer = UpdatePaymentStatusSerializer(
            data=request.data, context={'payment': payment}
        )
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        payment.status = new_status

        if new_status == 'COMPLETED':
            payment.completed_at = timezone.now()

        transaction_ref = serializer.validated_data.get('transaction_reference')
        if transaction_ref:
            payment.transaction_reference = transaction_ref

        notes = serializer.validated_data.get('notes')
        if notes:
            payment.notes = notes

        payment.save()

        return success_response(
            data=PaymentRecordSerializer(payment).data,
            message=f'Payment status updated to {new_status}.',
        )
