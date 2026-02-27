from rest_framework import serializers
from django.utils import timezone
from .models import Competition, CompetitionQuestion, CompetitionBookmark


class CompetitionQuestionReadSerializer(serializers.ModelSerializer):
    """Read-only serializer for questions."""
    asked_by_username = serializers.CharField(source='asked_by.username', read_only=True)
    answered_by_username = serializers.CharField(
        source='answered_by.username', read_only=True, default=None
    )

    class Meta:
        model = CompetitionQuestion
        fields = [
            'id', 'question', 'answer', 'asked_by_username',
            'answered_by_username', 'answered_at', 'is_public', 'created_at',
        ]


class CompetitionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for competition list views."""
    client_username = serializers.CharField(source='client.username', read_only=True)
    proposal_count = serializers.ReadOnlyField()
    is_open = serializers.ReadOnlyField()

    class Meta:
        model = Competition
        fields = [
            'id', 'title', 'client_username', 'budget', 'currency',
            'deadline', 'status', 'category', 'proposal_count',
            'is_open', 'created_at',
        ]


class CompetitionDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer for a single competition."""
    client_username = serializers.CharField(source='client.username', read_only=True)
    client_profile_picture = serializers.ImageField(
        source='client.profile_picture', read_only=True
    )
    proposal_count = serializers.ReadOnlyField()
    is_open = serializers.ReadOnlyField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = [
            'id', 'client', 'client_username', 'client_profile_picture',
            'title', 'description', 'requirements', 'budget', 'currency',
            'deadline', 'submission_deadline', 'status', 'category', 'tags',
            'max_proposals', 'allow_questions', 'proposal_count', 'is_open',
            'winner', 'winning_proposal',
            'created_at', 'updated_at', 'questions',
        ]

    def get_questions(self, obj):
        public_questions = obj.questions.filter(is_public=True)
        return CompetitionQuestionReadSerializer(public_questions, many=True).data


class CompetitionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a competition."""

    class Meta:
        model = Competition
        fields = [
            'id', 'title', 'description', 'requirements', 'budget',
            'currency', 'deadline', 'submission_deadline', 'category',
            'tags', 'max_proposals', 'allow_questions',
        ]
        read_only_fields = ['id']

    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Deadline must be in the future.')
        return value

    def validate_submission_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Submission deadline must be in the future.')
        return value

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError('Budget must be a positive number.')
        return value

    def validate_max_proposals(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Max proposals must be a positive number.')
        return value

    def validate(self, data):
        submission_deadline = data.get('submission_deadline')
        deadline = data.get('deadline')
        if submission_deadline and deadline and submission_deadline >= deadline:
            raise serializers.ValidationError({
                'submission_deadline': 'Submission deadline must be before the competition deadline.'
            })
        return data

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user
        validated_data['status'] = 'DRAFT'
        return super().create(validated_data)


class CompetitionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a competition (client owner only)."""

    class Meta:
        model = Competition
        fields = [
            'title', 'description', 'requirements', 'budget',
            'deadline', 'submission_deadline', 'tags', 'max_proposals',
            'allow_questions', 'category',
        ]

    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Deadline must be in the future.')
        return value

    def validate_submission_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError('Submission deadline must be in the future.')
        return value

    def validate_budget(self, value):
        if value <= 0:
            raise serializers.ValidationError('Budget must be a positive number.')
        return value

    def validate_max_proposals(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError('Max proposals must be a positive number.')
        return value

    def validate(self, data):
        instance = self.instance
        submission_deadline = data.get('submission_deadline', instance.submission_deadline if instance else None)
        deadline = data.get('deadline', instance.deadline if instance else None)
        if submission_deadline and deadline and submission_deadline >= deadline:
            raise serializers.ValidationError({
                'submission_deadline': 'Submission deadline must be before the competition deadline.'
            })
        return data


class CompetitionStatusSerializer(serializers.Serializer):
    """Serializer for changing competition status with state machine validation."""
    status = serializers.ChoiceField(
        choices=['DRAFT', 'OPEN', 'REVIEW', 'CLOSED', 'CANCELLED']
    )

    VALID_TRANSITIONS = {
        'DRAFT': ['OPEN', 'CANCELLED'],
        'OPEN': ['REVIEW', 'CANCELLED'],
        'REVIEW': ['CLOSED'],
        'CLOSED': [],
        'CANCELLED': [],
    }

    def validate_status(self, value):
        competition = self.context.get('competition')
        if not competition:
            raise serializers.ValidationError('Competition context is required.')

        current_status = competition.status
        allowed = self.VALID_TRANSITIONS.get(current_status, [])

        if value not in allowed:
            raise serializers.ValidationError(
                f'Cannot transition from {current_status} to {value}. '
                f'Allowed transitions: {", ".join(allowed) if allowed else "none (terminal state)"}.'
            )
        return value


class CompetitionQuestionSerializer(serializers.ModelSerializer):
    """Serializer for creating and reading questions."""
    asked_by_username = serializers.CharField(source='asked_by.username', read_only=True)

    class Meta:
        model = CompetitionQuestion
        fields = [
            'id', 'competition', 'question', 'asked_by_username',
            'answer', 'answered_at', 'is_public', 'created_at',
        ]
        read_only_fields = ['id', 'competition', 'answer', 'answered_at', 'is_public', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.user.role != 'FREELANCER':
            raise serializers.ValidationError('Only freelancers can ask questions.')
        return data

    def create(self, validated_data):
        validated_data['asked_by'] = self.context['request'].user
        validated_data['competition'] = self.context['competition']
        return super().create(validated_data)


class CompetitionAnswerSerializer(serializers.Serializer):
    """Serializer for answering a question."""
    answer = serializers.CharField()
    is_public = serializers.BooleanField(default=True)

    def validate(self, data):
        request = self.context.get('request')
        question = self.context.get('question')
        if question and question.competition.client != request.user:
            raise serializers.ValidationError('Only the competition client can answer questions.')
        return data


class CompetitionBookmarkSerializer(serializers.ModelSerializer):
    """Serializer for competition bookmarks."""

    class Meta:
        model = CompetitionBookmark
        fields = ['id', 'competition', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
