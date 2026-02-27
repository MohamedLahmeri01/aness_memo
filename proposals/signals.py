from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Proposal


@receiver(post_save, sender=Proposal)
def proposal_post_save(sender, instance, created, **kwargs):
    """Handle proposal creation and score update notifications."""
    if created:
        from notifications.utils import NotificationService
        NotificationService.notify_proposal_received(instance.competition, instance)

    # Check if client_score was updated (use update_fields if available)
    update_fields = kwargs.get('update_fields')
    if update_fields and 'client_score' in update_fields and instance.client_score:
        from notifications.utils import NotificationService
        NotificationService.notify_proposal_scored(instance)
