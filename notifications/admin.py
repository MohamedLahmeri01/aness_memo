from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'recipient', 'notification_type', 'title',
        'is_read', 'created_at',
    )
    list_filter = ('is_read', 'notification_type')
    search_fields = ('title', 'message')
    readonly_fields = ('id', 'created_at')

    actions = ['mark_all_read']

    @admin.action(description='Mark selected notifications as read')
    def mark_all_read(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(is_read=False).update(
            is_read=True, read_at=timezone.now()
        )
        self.message_user(request, f'{updated} notification(s) marked as read.')
