import uuid
from django.db import models
from django.conf import settings


class Proposal(models.Model):
    """Freelancer submission/proposal for a competition."""

    STATUS_CHOICES = (
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(
        'competitions.Competition',
        on_delete=models.CASCADE,
        related_name='proposals',
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proposals',
        limit_choices_to={'role': 'FREELANCER'},
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    proposed_budget = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_duration = models.PositiveIntegerField(help_text='Duration in days')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    submission_note = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_score = models.PositiveIntegerField(null=True, blank=True)
    client_note = models.TextField(null=True, blank=True)
    is_winner = models.BooleanField(default=False)

    class Meta:
        db_table = 'proposals_proposal'
        unique_together = ('competition', 'freelancer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.freelancer.username} for {self.competition.title}"


class ProposalAttachment(models.Model):
    """File attachments for proposals."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, related_name='attachments'
    )
    file = models.FileField(upload_to='proposal_attachments/')
    original_filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField(help_text='File size in bytes')
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        db_table = 'proposals_proposalattachment'

    def __str__(self):
        return f"{self.original_filename} for {self.proposal.title}"


class ProposalRevision(models.Model):
    """Tracks revisions made to proposals."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proposal = models.ForeignKey(
        Proposal, on_delete=models.CASCADE, related_name='revisions'
    )
    revised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    description = models.TextField()
    revision_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proposals_proposalrevision'
        ordering = ['-revision_number']

    def __str__(self):
        return f"Revision {self.revision_number} for {self.proposal.title}"
