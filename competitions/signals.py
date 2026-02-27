from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Competition


@receiver(post_save, sender=Competition)
def competition_status_changed(sender, instance, created, **kwargs):
    """When competition status changes to OPEN, notify bookmarked users."""
    if not created and instance.status == 'OPEN':
        from notifications.utils import NotificationService
        from .models import CompetitionBookmark

        bookmarks = CompetitionBookmark.objects.filter(competition=instance)
        for bookmark in bookmarks:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=bookmark.user,
                notification_type='COMPETITION_OPENED',
                title=f'Competition Now Open: {instance.title}',
                message=f'The competition "{instance.title}" you bookmarked is now open for submissions.',
                related_competition_id=instance.id,
            )
