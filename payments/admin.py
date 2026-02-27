from django.contrib import admin
from .models import PaymentRecord


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        'competition', 'client', 'freelancer', 'amount',
        'currency', 'status', 'platform_fee', 'net_amount', 'created_at',
    )
    list_filter = ('status', 'currency')
    search_fields = ('transaction_reference', 'notes')
    readonly_fields = ('id', 'created_at', 'updated_at', 'platform_fee', 'net_amount')

    actions = ['mark_completed', 'mark_failed']

    @admin.action(description='Mark selected payments as completed')
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='PROCESSING').update(
            status='COMPLETED', completed_at=timezone.now()
        )
        self.message_user(request, f'{updated} payment(s) marked as completed.')

    @admin.action(description='Mark selected payments as failed')
    def mark_failed(self, request, queryset):
        updated = queryset.filter(status='PROCESSING').update(status='FAILED')
        self.message_user(request, f'{updated} payment(s) marked as failed.')
