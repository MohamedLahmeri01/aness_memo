import uuid
from django.db import models
from django.conf import settings
from django.db.models import Avg


class Review(models.Model):
    """Post-competition review between client and freelancer."""

    REVIEW_TYPE_CHOICES = (
        ('CLIENT_TO_FREELANCER', 'Client to Freelancer'),
        ('FREELANCER_TO_CLIENT', 'Freelancer to Client'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_given',
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_received',
    )
    competition = models.ForeignKey(
        'competitions.Competition',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    review_type = models.CharField(max_length=30, choices=REVIEW_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        db_table = 'feedback_review'
        unique_together = ('reviewer', 'competition')
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username}"


class UserRating(models.Model):
    """Denormalized user rating for performance."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rating',
        primary_key=True,
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedback_userrating'

    def __str__(self):
        return f"Rating for {self.user.username}: {self.average_rating}"

    @classmethod
    def update_for_user(cls, user_id):
        """Recalculate and save the average rating for a user."""
        from .models import Review
        reviews = Review.objects.filter(reviewee_id=user_id, is_public=True)
        aggregation = reviews.aggregate(avg=Avg('rating'))
        avg_rating = aggregation['avg'] or 0.00
        total = reviews.count()

        rating_obj, _ = cls.objects.get_or_create(user_id=user_id)
        rating_obj.average_rating = round(avg_rating, 2)
        rating_obj.total_reviews = total
        rating_obj.save(update_fields=['average_rating', 'total_reviews', 'updated_at'])
        return rating_obj
