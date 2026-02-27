from rest_framework import serializers
from .models import Review, UserRating


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a review."""

    class Meta:
        model = Review
        fields = ['id', 'competition', 'reviewee', 'rating', 'comment', 'is_public']
        read_only_fields = ['id']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def validate(self, data):
        request = self.context.get('request')
        competition = data.get('competition')
        reviewer = request.user

        # Competition must be CLOSED
        if competition.status != 'CLOSED':
            raise serializers.ValidationError(
                {'competition': 'Reviews can only be submitted for closed competitions.'}
            )

        # Check for duplicate review
        if Review.objects.filter(reviewer=reviewer, competition=competition).exists():
            raise serializers.ValidationError(
                {'competition': 'You have already reviewed this competition.'}
            )

        # Check reviewer participated
        is_client = competition.client == reviewer
        from proposals.models import Proposal
        is_freelancer = Proposal.objects.filter(
            competition=competition, freelancer=reviewer
        ).exists()

        if not is_client and not is_freelancer:
            raise serializers.ValidationError(
                'You must have participated in this competition to leave a review.'
            )

        # Determine review type and validate reviewee
        reviewee = data.get('reviewee')
        if is_client:
            data['review_type'] = 'CLIENT_TO_FREELANCER'
            # Validate reviewee is a freelancer who submitted a proposal
            if not Proposal.objects.filter(
                competition=competition, freelancer=reviewee
            ).exists():
                raise serializers.ValidationError(
                    {'reviewee': 'Reviewee must be a freelancer who participated in this competition.'}
                )
        else:
            data['review_type'] = 'FREELANCER_TO_CLIENT'
            if reviewee != competition.client:
                raise serializers.ValidationError(
                    {'reviewee': 'As a freelancer, you can only review the competition client.'}
                )

        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Full read-only review serializer."""
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    reviewer_profile_picture = serializers.ImageField(
        source='reviewer.profile_picture', read_only=True
    )
    reviewee_username = serializers.CharField(source='reviewee.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewer_username', 'reviewer_profile_picture',
            'reviewee', 'reviewee_username', 'competition', 'rating',
            'comment', 'review_type', 'created_at', 'is_public',
        ]


class UserRatingSerializer(serializers.ModelSerializer):
    """Read-only user rating serializer."""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserRating
        fields = ['user', 'username', 'average_rating', 'total_reviews', 'updated_at']
