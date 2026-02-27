from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from freelance_arena.utils import success_response
from accounts.permissions import IsClient
from .models import Competition, CompetitionQuestion, CompetitionBookmark
from .serializers import (
    CompetitionListSerializer,
    CompetitionDetailSerializer,
    CompetitionCreateSerializer,
    CompetitionUpdateSerializer,
    CompetitionStatusSerializer,
    CompetitionQuestionSerializer,
    CompetitionQuestionReadSerializer,
    CompetitionAnswerSerializer,
    CompetitionBookmarkSerializer,
)
from .filters import CompetitionFilter


class CompetitionListView(generics.ListAPIView):
    """GET - List all OPEN competitions. Public access."""
    serializer_class = CompetitionListSerializer
    permission_classes = [AllowAny]
    filterset_class = CompetitionFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category']
    ordering_fields = ['budget', 'deadline', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Competition.objects.filter(status='OPEN')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Competitions retrieved.')


class CompetitionCreateView(APIView):
    """POST - Create a new competition. CLIENT only."""
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request):
        serializer = CompetitionCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        competition = serializer.save()
        return success_response(
            data=CompetitionDetailSerializer(competition).data,
            message='Competition created successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class CompetitionDetailView(APIView):
    """GET/PUT/PATCH/DELETE a competition."""
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        serializer = CompetitionDetailSerializer(competition)
        return success_response(data=serializer.data, message='Competition detail retrieved.')

    def put(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='You are not the owner of this competition.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if competition.status not in ('DRAFT', 'OPEN'):
            return success_response(
                data=None, message='Competition can only be updated when in DRAFT or OPEN status.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CompetitionUpdateSerializer(competition, data=request.data)
        serializer.is_valid(raise_exception=True)
        competition = serializer.save()
        return success_response(
            data=CompetitionDetailSerializer(competition).data,
            message='Competition updated.',
        )

    def patch(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='You are not the owner of this competition.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if competition.status not in ('DRAFT', 'OPEN'):
            return success_response(
                data=None, message='Competition can only be updated when in DRAFT or OPEN status.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CompetitionUpdateSerializer(competition, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        competition = serializer.save()
        return success_response(
            data=CompetitionDetailSerializer(competition).data,
            message='Competition updated.',
        )

    def delete(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='You are not the owner of this competition.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if competition.status != 'DRAFT':
            return success_response(
                data=None, message='Only DRAFT competitions can be deleted (cancelled).',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        competition.status = 'CANCELLED'
        competition.save(update_fields=['status'])
        return success_response(message='Competition cancelled.')


class CompetitionStatusView(APIView):
    """POST - Change competition status. CLIENT owner only."""
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='You are not the owner of this competition.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        serializer = CompetitionStatusSerializer(
            data=request.data, context={'competition': competition}
        )
        serializer.is_valid(raise_exception=True)
        competition.status = serializer.validated_data['status']
        competition.save(update_fields=['status', 'updated_at'])
        return success_response(
            data=CompetitionDetailSerializer(competition).data,
            message=f'Competition status changed to {competition.status}.',
        )


class MyCompetitionsView(generics.ListAPIView):
    """GET - List own competitions. CLIENT only."""
    serializer_class = CompetitionListSerializer
    permission_classes = [IsAuthenticated, IsClient]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'deadline', 'budget']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Competition.objects.filter(client=self.request.user)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Your competitions retrieved.')


class CompetitionQuestionListCreateView(APIView):
    """GET - list public questions. POST - ask a question (FREELANCER only)."""

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        questions = competition.questions.filter(is_public=True)
        serializer = CompetitionQuestionReadSerializer(questions, many=True)
        return success_response(data=serializer.data, message='Questions retrieved.')

    def post(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if not competition.allow_questions:
            return success_response(
                data=None, message='Questions are not allowed for this competition.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        if competition.status != 'OPEN':
            return success_response(
                data=None, message='Questions can only be asked on OPEN competitions.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CompetitionQuestionSerializer(
            data=request.data,
            context={'request': request, 'competition': competition},
        )
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        return success_response(
            data=CompetitionQuestionReadSerializer(question).data,
            message='Question submitted.',
            status_code=status.HTTP_201_CREATED,
        )


class CompetitionAnswerView(APIView):
    """POST - Answer a question. Competition CLIENT owner only."""
    permission_classes = [IsAuthenticated]

    def post(self, request, competition_id, question_id):
        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='Only the competition owner can answer questions.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        question = get_object_or_404(
            CompetitionQuestion, id=question_id, competition=competition
        )
        serializer = CompetitionAnswerSerializer(
            data=request.data,
            context={'request': request, 'question': question},
        )
        serializer.is_valid(raise_exception=True)

        question.answer = serializer.validated_data['answer']
        question.is_public = serializer.validated_data.get('is_public', True)
        question.answered_by = request.user
        question.answered_at = timezone.now()
        question.save()

        # Send notification
        from notifications.utils import NotificationService
        NotificationService.notify_question_answered(question)

        return success_response(
            data=CompetitionQuestionReadSerializer(question).data,
            message='Question answered.',
        )


class CompetitionBookmarkView(APIView):
    """POST - Toggle bookmark. GET - List bookmarked competitions."""
    permission_classes = [IsAuthenticated]

    def post(self, request, competition_id):
        competition = get_object_or_404(Competition, id=competition_id)
        bookmark, created = CompetitionBookmark.objects.get_or_create(
            competition=competition, user=request.user
        )
        if not created:
            bookmark.delete()
            return success_response(message='Bookmark removed.')
        return success_response(
            message='Competition bookmarked.',
            status_code=status.HTTP_201_CREATED,
        )


class BookmarkListView(generics.ListAPIView):
    """GET - List all bookmarked competitions."""
    serializer_class = CompetitionListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        bookmark_competition_ids = CompetitionBookmark.objects.filter(
            user=self.request.user
        ).values_list('competition_id', flat=True)
        return Competition.objects.filter(id__in=bookmark_competition_ids)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Bookmarked competitions retrieved.')


class SelectWinnerView(APIView):
    """POST - Select the winning proposal. CLIENT owner only."""
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, competition_id):
        from proposals.models import Proposal

        competition = get_object_or_404(Competition, id=competition_id)
        if competition.client != request.user:
            return success_response(
                data=None, message='You are not the owner of this competition.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if competition.status != 'REVIEW':
            return success_response(
                data=None, message='Winner can only be selected when competition is in REVIEW status.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        proposal_id = request.data.get('proposal_id')
        if not proposal_id:
            return success_response(
                data=None, message='proposal_id is required.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            proposal = Proposal.objects.get(id=proposal_id, competition=competition)
        except Proposal.DoesNotExist:
            return success_response(
                data=None, message='Proposal not found for this competition.',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if proposal.status == 'WITHDRAWN':
            return success_response(
                data=None, message='Cannot select a withdrawn proposal.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Set the winner
        competition.winning_proposal = proposal
        competition.winner = proposal.freelancer
        competition.status = 'CLOSED'
        competition.save(update_fields=['winning_proposal', 'winner', 'status', 'updated_at'])

        # Update proposal statuses
        proposal.is_winner = True
        proposal.status = 'ACCEPTED'
        proposal.save(update_fields=['is_winner', 'status', 'updated_at'])

        # Reject all other proposals
        competition.proposals.exclude(id=proposal.id).update(status='REJECTED')

        # Create payment record
        from payments.models import PaymentRecord
        PaymentRecord.objects.create(
            competition=competition,
            client=competition.client,
            freelancer=proposal.freelancer,
            amount=competition.budget,
            currency=competition.currency,
        )

        # Send notifications
        from notifications.utils import NotificationService
        NotificationService.notify_winner_selected(competition, proposal)
        NotificationService.notify_competition_closed(competition)

        return success_response(
            data=CompetitionDetailSerializer(competition).data,
            message='Winner selected and competition closed.',
        )
