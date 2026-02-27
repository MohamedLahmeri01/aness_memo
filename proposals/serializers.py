import os
from rest_framework import serializers
from django.utils import timezone
from .models import Proposal, ProposalAttachment, ProposalRevision


ALLOWED_FILE_TYPES = ['pdf', 'doc', 'docx', 'zip', 'jpg', 'jpeg', 'png', 'mp4']


class ProposalAttachmentSerializer(serializers.ModelSerializer):
    """Serializer for proposal file attachments."""

    class Meta:
        model = ProposalAttachment
        fields = [
            'id', 'file', 'original_filename', 'file_size',
            'file_type', 'uploaded_at', 'description',
        ]
        read_only_fields = ['id', 'original_filename', 'file_size', 'file_type', 'uploaded_at']

    def validate_file(self, value):
        # Validate file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('File size must be less than 10MB.')

        # Validate file type
        ext = os.path.splitext(value.name)[1].lower().lstrip('.')
        if ext not in ALLOWED_FILE_TYPES:
            raise serializers.ValidationError(
                f'File type .{ext} is not allowed. Allowed types: {", ".join(ALLOWED_FILE_TYPES)}'
            )
        return value

    def create(self, validated_data):
        file_obj = validated_data['file']
        validated_data['original_filename'] = file_obj.name
        validated_data['file_size'] = file_obj.size
        ext = os.path.splitext(file_obj.name)[1].lower().lstrip('.')
        validated_data['file_type'] = ext
        return super().create(validated_data)


class ProposalCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a proposal."""
    attachments = ProposalAttachmentSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id', 'competition', 'title', 'description',
            'proposed_budget', 'estimated_duration', 'submission_note',
            'attachments',
        ]
        read_only_fields = ['id']

    def validate_proposed_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError('Proposed budget must be positive.')
        return value

    def validate(self, data):
        request = self.context.get('request')
        competition = data.get('competition')

        # Check competition is OPEN
        if competition.status != 'OPEN':
            raise serializers.ValidationError(
                {'competition': 'Competition is not open for submissions.'}
            )

        # Check submission deadline
        if competition.submission_deadline <= timezone.now():
            raise serializers.ValidationError(
                {'competition': 'Submission deadline has passed.'}
            )

        # Check unique proposal
        if Proposal.objects.filter(
            competition=competition, freelancer=request.user
        ).exists():
            raise serializers.ValidationError(
                {'competition': 'You have already submitted a proposal for this competition.'}
            )

        # Check max_proposals limit
        if competition.max_proposals is not None:
            current_count = competition.proposals.exclude(status='WITHDRAWN').count()
            if current_count >= competition.max_proposals:
                raise serializers.ValidationError(
                    {'competition': 'Maximum number of proposals has been reached.'}
                )

        return data

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        validated_data['freelancer'] = self.context['request'].user
        proposal = Proposal.objects.create(**validated_data)

        for attachment_data in attachments_data:
            file_obj = attachment_data['file']
            ProposalAttachment.objects.create(
                proposal=proposal,
                file=file_obj,
                original_filename=file_obj.name,
                file_size=file_obj.size,
                file_type=os.path.splitext(file_obj.name)[1].lower().lstrip('.'),
                description=attachment_data.get('description', ''),
            )

        return proposal


class ProposalDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer for proposal."""
    attachments = ProposalAttachmentSerializer(many=True, read_only=True)
    freelancer_username = serializers.CharField(source='freelancer.username', read_only=True)
    competition_title = serializers.CharField(source='competition.title', read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id', 'competition', 'competition_title', 'freelancer',
            'freelancer_username', 'title', 'description',
            'proposed_budget', 'estimated_duration', 'status',
            'submission_note', 'created_at', 'updated_at',
            'client_score', 'client_note', 'is_winner', 'attachments',
        ]


class ProposalListSerializer(serializers.ModelSerializer):
    """Lightweight list serializer for freelancer's own proposals."""
    competition_title = serializers.CharField(source='competition.title', read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id', 'competition', 'competition_title', 'title',
            'status', 'created_at', 'proposed_budget',
        ]


class ClientProposalListSerializer(serializers.ModelSerializer):
    """For client viewing proposals - blind review (no freelancer identity)."""

    class Meta:
        model = Proposal
        fields = [
            'id', 'title', 'proposed_budget', 'estimated_duration',
            'created_at', 'client_score', 'description',
        ]


class ClientScoreSerializer(serializers.Serializer):
    """For client to add score and feedback to a proposal."""
    client_score = serializers.IntegerField(min_value=1, max_value=5)
    client_note = serializers.CharField(required=False, allow_blank=True, default='')

    def validate(self, data):
        proposal = self.context.get('proposal')
        if proposal:
            competition = proposal.competition
            if competition.status not in ('OPEN', 'REVIEW'):
                raise serializers.ValidationError(
                    'Scoring is only allowed when competition is OPEN or in REVIEW.'
                )
        return data


class ProposalWithdrawSerializer(serializers.Serializer):
    """For freelancer to withdraw their proposal."""

    def validate(self, data):
        proposal = self.context.get('proposal')
        if proposal and proposal.status != 'SUBMITTED':
            raise serializers.ValidationError(
                'Only proposals with SUBMITTED status can be withdrawn.'
            )
        return data


class ProposalRevisionSerializer(serializers.ModelSerializer):
    """Serializer for proposal revisions."""

    class Meta:
        model = ProposalRevision
        fields = ['id', 'description', 'revision_number', 'created_at']
        read_only_fields = ['id', 'revision_number', 'created_at']
