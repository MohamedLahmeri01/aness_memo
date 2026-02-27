from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from freelance_arena.utils import success_response
from accounts.permissions import IsFreelancer, IsClient
from .models import Proposal, ProposalAttachment
from .serializers import (
    ProposalCreateSerializer,
    ProposalDetailSerializer,
    ProposalListSerializer,
    ClientProposalListSerializer,
    ClientScoreSerializer,
    ProposalWithdrawSerializer,
    ProposalAttachmentSerializer,
)


class ProposalCreateView(APIView):
    """POST - Submit a proposal. FREELANCER only."""
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request):
        serializer = ProposalCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        proposal = serializer.save()
        return success_response(
            data=ProposalDetailSerializer(proposal).data,
            message='Proposal submitted successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class MyProposalsView(generics.ListAPIView):
    """GET - List own proposals. FREELANCER only."""
    serializer_class = ProposalListSerializer
    permission_classes = [IsAuthenticated, IsFreelancer]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'proposed_budget']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Proposal.objects.filter(freelancer=self.request.user)
        competition_id = self.request.query_params.get('competition')
        status_filter = self.request.query_params.get('status')
        if competition_id:
            queryset = queryset.filter(competition_id=competition_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter.upper())
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Your proposals retrieved.')


class ProposalDetailView(APIView):
    """GET/PUT/DELETE a proposal."""
    permission_classes = [IsAuthenticated]

    def get(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        # Access control: freelancer owner or competition client
        if (proposal.freelancer != request.user and
                proposal.competition.client != request.user and
                request.user.role != 'ADMIN'):
            return success_response(
                data=None, message='You do not have permission to view this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProposalDetailSerializer(proposal)
        return success_response(data=serializer.data, message='Proposal detail retrieved.')

    def put(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.freelancer != request.user:
            return success_response(
                data=None, message='You are not the owner of this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if proposal.status != 'SUBMITTED':
            return success_response(
                data=None, message='Only SUBMITTED proposals can be updated.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        allowed_fields = ['title', 'description', 'proposed_budget', 'estimated_duration', 'submission_note']
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}

        for field, value in update_data.items():
            setattr(proposal, field, value)
        proposal.save()

        return success_response(
            data=ProposalDetailSerializer(proposal).data,
            message='Proposal updated.',
        )

    def delete(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.freelancer != request.user:
            return success_response(
                data=None, message='You are not the owner of this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        proposal.status = 'WITHDRAWN'
        proposal.save(update_fields=['status', 'updated_at'])
        return success_response(message='Proposal withdrawn.')


class AddAttachmentView(APIView):
    """POST - Add attachment to proposal. FREELANCER owner only."""
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.freelancer != request.user:
            return success_response(
                data=None, message='You are not the owner of this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if proposal.status != 'SUBMITTED':
            return success_response(
                data=None, message='Attachments can only be added to SUBMITTED proposals.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProposalAttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(proposal=proposal)

        return success_response(
            data=serializer.data,
            message='Attachment added.',
            status_code=status.HTTP_201_CREATED,
        )


class DeleteAttachmentView(APIView):
    """DELETE - Remove attachment from proposal. FREELANCER owner only."""
    permission_classes = [IsAuthenticated, IsFreelancer]

    def delete(self, request, proposal_id, attachment_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.freelancer != request.user:
            return success_response(
                data=None, message='You are not the owner of this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )
        if proposal.status != 'SUBMITTED':
            return success_response(
                data=None, message='Attachments can only be removed from SUBMITTED proposals.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        attachment = get_object_or_404(
            ProposalAttachment, id=attachment_id, proposal=proposal
        )
        attachment.delete()
        return success_response(message='Attachment deleted.')


class CompetitionProposalsView(generics.ListAPIView):
    """GET - List proposals for a competition. CLIENT owner only (blind review)."""
    serializer_class = ClientProposalListSerializer
    permission_classes = [IsAuthenticated, IsClient]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['client_score', 'created_at', 'proposed_budget']
    ordering = ['-created_at']

    def get_queryset(self):
        from competitions.models import Competition
        competition = get_object_or_404(
            Competition, id=self.kwargs['competition_id']
        )
        if competition.client != self.request.user:
            return Proposal.objects.none()
        return Proposal.objects.filter(competition=competition).exclude(status='WITHDRAWN')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Competition proposals retrieved.')


class ScoreProposalView(APIView):
    """POST - Score a proposal. Competition CLIENT owner only."""
    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.competition.client != request.user:
            return success_response(
                data=None, message='Only the competition owner can score proposals.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = ClientScoreSerializer(
            data=request.data, context={'proposal': proposal}
        )
        serializer.is_valid(raise_exception=True)

        proposal.client_score = serializer.validated_data['client_score']
        proposal.client_note = serializer.validated_data.get('client_note', '')
        proposal.save(update_fields=['client_score', 'client_note', 'updated_at'])

        return success_response(
            data=ClientProposalListSerializer(proposal).data,
            message='Proposal scored.',
        )


class WithdrawProposalView(APIView):
    """POST - Withdraw own proposal. FREELANCER owner only."""
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request, proposal_id):
        proposal = get_object_or_404(Proposal, id=proposal_id)

        if proposal.freelancer != request.user:
            return success_response(
                data=None, message='You are not the owner of this proposal.',
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProposalWithdrawSerializer(
            data={}, context={'proposal': proposal}
        )
        serializer.is_valid(raise_exception=True)

        proposal.status = 'WITHDRAWN'
        proposal.save(update_fields=['status', 'updated_at'])
        return success_response(message='Proposal withdrawn.')
