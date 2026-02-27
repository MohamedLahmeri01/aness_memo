from .models import Notification


class NotificationService:
    """Service class for creating notifications."""

    @staticmethod
    def notify_proposal_received(competition, proposal):
        """Notify the client that a new proposal was received."""
        Notification.objects.create(
            recipient=competition.client,
            notification_type='PROPOSAL_RECEIVED',
            title=f'New Proposal Received',
            message=f'A new proposal "{proposal.title}" has been submitted to your competition "{competition.title}".',
            related_competition_id=competition.id,
            related_proposal_id=proposal.id,
        )

    @staticmethod
    def notify_proposal_scored(proposal):
        """Notify the freelancer that their proposal was scored."""
        Notification.objects.create(
            recipient=proposal.freelancer,
            notification_type='PROPOSAL_SCORED',
            title='Your Proposal Was Scored',
            message=f'Your proposal "{proposal.title}" for "{proposal.competition.title}" received a score of {proposal.client_score}/5.',
            related_competition_id=proposal.competition_id,
            related_proposal_id=proposal.id,
        )

    @staticmethod
    def notify_winner_selected(competition, winning_proposal):
        """Notify the winner and all losing freelancers."""
        # Notify the winner
        Notification.objects.create(
            recipient=winning_proposal.freelancer,
            notification_type='WINNER_SELECTED',
            title='Congratulations! You Won!',
            message=f'Your proposal "{winning_proposal.title}" was selected as the winner for "{competition.title}"!',
            related_competition_id=competition.id,
            related_proposal_id=winning_proposal.id,
        )

        # Notify losing freelancers
        from proposals.models import Proposal
        losing_proposals = Proposal.objects.filter(
            competition=competition
        ).exclude(
            id=winning_proposal.id
        ).exclude(
            status='WITHDRAWN'
        ).select_related('freelancer')

        for proposal in losing_proposals:
            Notification.objects.create(
                recipient=proposal.freelancer,
                notification_type='PROPOSAL_REJECTED',
                title='Competition Result',
                message=f'The competition "{competition.title}" has been decided. Unfortunately, your proposal was not selected.',
                related_competition_id=competition.id,
                related_proposal_id=proposal.id,
            )

    @staticmethod
    def notify_question_answered(question):
        """Notify the freelancer who asked the question."""
        Notification.objects.create(
            recipient=question.asked_by,
            notification_type='QUESTION_ANSWERED',
            title='Your Question Was Answered',
            message=f'Your question on "{question.competition.title}" has been answered.',
            related_competition_id=question.competition_id,
        )

    @staticmethod
    def notify_competition_closed(competition):
        """Notify all participating freelancers that the competition is closed."""
        from proposals.models import Proposal
        proposals = Proposal.objects.filter(
            competition=competition
        ).exclude(
            status='WITHDRAWN'
        ).select_related('freelancer')

        notified_users = set()
        for proposal in proposals:
            if proposal.freelancer_id not in notified_users:
                Notification.objects.create(
                    recipient=proposal.freelancer,
                    notification_type='COMPETITION_CLOSED',
                    title='Competition Closed',
                    message=f'The competition "{competition.title}" has been closed.',
                    related_competition_id=competition.id,
                )
                notified_users.add(proposal.freelancer_id)

    @staticmethod
    def notify_new_review(review):
        """Notify the reviewee about a new review."""
        Notification.objects.create(
            recipient=review.reviewee,
            notification_type='NEW_REVIEW',
            title='New Review Received',
            message=f'You received a new {review.rating}/5 star review from {review.reviewer.username}.',
            related_competition_id=review.competition_id,
        )
