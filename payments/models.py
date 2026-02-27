import uuid
from django.db import models
from django.conf import settings


class PaymentRecord(models.Model):
    """Payment tracking for completed competitions."""

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.OneToOneField(
        'competitions.Competition',
        on_delete=models.CASCADE,
        related_name='payment',
    )
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments_made',
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments_received',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    transaction_reference = models.CharField(
        max_length=100, unique=True, null=True, blank=True
    )
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'payments_paymentrecord'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for {self.competition.title} - {self.status}"

    def save(self, *args, **kwargs):
        """Auto-calculate platform_fee (10%) and net_amount."""
        from decimal import Decimal
        if self.amount:
            self.platform_fee = (self.amount * Decimal('0.10')).quantize(Decimal('0.01'))
            self.net_amount = (self.amount - self.platform_fee).quantize(Decimal('0.01'))
        super().save(*args, **kwargs)
