from django.core.management.base import BaseCommand
from django.utils import timezone
from competitions.models import Competition
from notifications.utils import NotificationService
from proposals.models import Proposal


class Command(BaseCommand):
    help = 'Close competitions whose submission deadline has passed (OPEN -> REVIEW).'

    def handle(self, *args, **options):
        now = timezone.now()
        expired = Competition.objects.filter(
            status='OPEN',
            submission_deadline__lt=now,
        )

        count = expired.count()

        for competition in expired:
            competition.status = 'REVIEW'
            competition.save(update_fields=['status', 'updated_at'])

            # Notify participating freelancers
            proposals = Proposal.objects.filter(
                competition=competition
            ).exclude(
                status='WITHDRAWN'
            ).select_related('freelancer')

            for proposal in proposals:
                from notifications.models import Notification
                Notification.objects.create(
                    recipient=proposal.freelancer,
                    notification_type='COMPETITION_CLOSED',
                    title='Competition Moved to Review',
                    message=f'The competition "{competition.title}" submission period has ended and is now under review.',
                    related_competition_id=competition.id,
                )

        self.stdout.write(
            self.style.SUCCESS(f'{count} competition(s) moved from OPEN to REVIEW.')
        )
