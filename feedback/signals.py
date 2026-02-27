from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review, UserRating


@receiver(post_save, sender=Review)
def update_user_rating_on_review(sender, instance, created, **kwargs):
    """Update UserRating whenever a review is created or updated."""
    UserRating.update_for_user(instance.reviewee_id)

    # Send notification for new reviews
    if created:
        from notifications.utils import NotificationService
        NotificationService.notify_new_review(instance)
