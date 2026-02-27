import uuid
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """In-app notification for platform events."""

    NOTIFICATION_TYPES = (
        ('COMPETITION_OPENED', 'Competition Opened'),
        ('PROPOSAL_RECEIVED', 'Proposal Received'),
        ('PROPOSAL_SCORED', 'Proposal Scored'),
        ('PROPOSAL_ACCEPTED', 'Proposal Accepted'),
        ('PROPOSAL_REJECTED', 'Proposal Rejected'),
        ('COMPETITION_CLOSED', 'Competition Closed'),
        ('QUESTION_ANSWERED', 'Question Answered'),
        ('WINNER_SELECTED', 'Winner Selected'),
        ('NEW_REVIEW', 'New Review'),
        ('COMPETITION_DEADLINE_APPROACHING', 'Competition Deadline Approaching'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    related_competition_id = models.UUIDField(null=True, blank=True)
    related_proposal_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.recipient.username}"
