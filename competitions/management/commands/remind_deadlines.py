from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from competitions.models import Competition, CompetitionBookmark
from notifications.models import Notification
from proposals.models import Proposal


class Command(BaseCommand):
    help = 'Send deadline approaching notifications for competitions closing within 24 hours.'

    def handle(self, *args, **options):
        now = timezone.now()
        deadline_threshold = now + timedelta(hours=24)

        # Find OPEN competitions with deadline within 24 hours
        upcoming = Competition.objects.filter(
            status='OPEN',
            submission_deadline__gt=now,
            submission_deadline__lte=deadline_threshold,
        )

        total_notifications = 0

        for competition in upcoming:
            # Get freelancers who bookmarked but haven't submitted
            bookmarked_user_ids = CompetitionBookmark.objects.filter(
                competition=competition
            ).values_list('user_id', flat=True)

            submitted_user_ids = Proposal.objects.filter(
                competition=competition
            ).values_list('freelancer_id', flat=True)

            # Users who bookmarked but haven't submitted
            target_user_ids = set(bookmarked_user_ids) - set(submitted_user_ids)

            # Avoid duplicate notifications
            already_notified = Notification.objects.filter(
                notification_type='COMPETITION_DEADLINE_APPROACHING',
                related_competition_id=competition.id,
                recipient_id__in=target_user_ids,
            ).values_list('recipient_id', flat=True)

            remaining_ids = target_user_ids - set(already_notified)

            for user_id in remaining_ids:
                Notification.objects.create(
                    recipient_id=user_id,
                    notification_type='COMPETITION_DEADLINE_APPROACHING',
                    title='Deadline Approaching!',
                    message=f'The competition "{competition.title}" closes within 24 hours. Submit your proposal now!',
                    related_competition_id=competition.id,
                )
                total_notifications += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Sent {total_notifications} deadline reminder notification(s) '
                f'for {upcoming.count()} upcoming competition(s).'
            )
        )
