from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Full read-only notification serializer."""

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'title', 'message',
            'is_read', 'read_at', 'related_competition_id',
            'related_proposal_id', 'created_at',
        ]
        read_only_fields = fields


class MarkReadSerializer(serializers.Serializer):
    """Serializer for marking notifications as read."""
    notification_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
    )
