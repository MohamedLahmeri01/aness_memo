from rest_framework import serializers
from .models import PaymentRecord


class PaymentRecordSerializer(serializers.ModelSerializer):
    """Full payment detail serializer for admin."""
    competition_title = serializers.CharField(source='competition.title', read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    freelancer_username = serializers.CharField(
        source='freelancer.username', read_only=True, default=None
    )

    class Meta:
        model = PaymentRecord
        fields = [
            'id', 'competition', 'competition_title', 'client',
            'client_username', 'freelancer', 'freelancer_username',
            'amount', 'currency', 'status', 'platform_fee', 'net_amount',
            'created_at', 'updated_at', 'completed_at',
            'transaction_reference', 'notes',
        ]


class ClientPaymentSerializer(serializers.ModelSerializer):
    """Read-only serializer for client payment view."""
    competition_title = serializers.CharField(source='competition.title', read_only=True)

    class Meta:
        model = PaymentRecord
        fields = [
            'id', 'competition', 'competition_title', 'amount',
            'currency', 'status', 'created_at',
        ]


class FreelancerPaymentSerializer(serializers.ModelSerializer):
    """Read-only serializer for freelancer payment view."""
    competition_title = serializers.CharField(source='competition.title', read_only=True)

    class Meta:
        model = PaymentRecord
        fields = [
            'id', 'competition', 'competition_title', 'net_amount',
            'currency', 'status', 'completed_at',
        ]


class UpdatePaymentStatusSerializer(serializers.Serializer):
    """Serializer for updating payment status."""
    status = serializers.ChoiceField(
        choices=['PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'REFUNDED']
    )
    transaction_reference = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    VALID_TRANSITIONS = {
        'PENDING': ['PROCESSING'],
        'PROCESSING': ['COMPLETED', 'FAILED'],
        'COMPLETED': ['REFUNDED'],
        'FAILED': [],
        'REFUNDED': [],
    }

    def validate_status(self, value):
        payment = self.context.get('payment')
        if payment:
            current_status = payment.status
            allowed = self.VALID_TRANSITIONS.get(current_status, [])
            if value not in allowed:
                raise serializers.ValidationError(
                    f'Cannot transition from {current_status} to {value}. '
                    f'Allowed: {", ".join(allowed) if allowed else "none"}.'
                )
        return value
