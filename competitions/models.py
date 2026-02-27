import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Competition(models.Model):
    """Model representing a freelance competition/job posting."""

    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('OPEN', 'Open'),
        ('REVIEW', 'Review'),
        ('CLOSED', 'Closed'),
        ('CANCELLED', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='competitions',
        limit_choices_to={'role': 'CLIENT'},
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    deadline = models.DateTimeField()
    submission_deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    category = models.CharField(max_length=100)
    tags = models.TextField(blank=True, default='')
    max_proposals = models.PositiveIntegerField(null=True, blank=True)
    allow_questions = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='won_competitions',
    )
    winning_proposal = models.ForeignKey(
        'proposals.Proposal',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='won_for',
    )

    class Meta:
        db_table = 'competitions_competition'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.client.username}"

    @property
    def is_open(self):
        return self.status == 'OPEN' and self.submission_deadline > timezone.now()

    @property
    def proposal_count(self):
        return self.proposals.count()


class CompetitionQuestion(models.Model):
    """Questions asked by freelancers on competitions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='questions'
    )
    asked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions_asked',
    )
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='questions_answered',
    )
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'competitions_competitionquestion'
        ordering = ['-created_at']

    def __str__(self):
        return f"Q on {self.competition.title} by {self.asked_by.username}"


class CompetitionBookmark(models.Model):
    """Bookmarks for competitions."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='bookmarks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'competitions_competitionbookmark'
        unique_together = ('competition', 'user')

    def __str__(self):
        return f"{self.user.username} bookmarked {self.competition.title}"
