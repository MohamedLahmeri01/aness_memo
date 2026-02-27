from django.contrib import admin
from .models import Competition, CompetitionQuestion, CompetitionBookmark


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'client', 'status', 'budget', 'deadline',
        'proposal_count', 'created_at',
    )
    list_filter = ('status', 'category', 'currency')
    search_fields = ('title', 'description', 'category')
    readonly_fields = ('id', 'created_at', 'updated_at', 'proposal_count')
    ordering = ('-created_at',)

    actions = ['bulk_open', 'bulk_cancel']

    @admin.action(description='Open selected competitions')
    def bulk_open(self, request, queryset):
        updated = queryset.filter(status='DRAFT').update(status='OPEN')
        self.message_user(request, f'{updated} competition(s) opened.')

    @admin.action(description='Cancel selected competitions')
    def bulk_cancel(self, request, queryset):
        updated = queryset.exclude(status__in=['CLOSED', 'CANCELLED']).update(status='CANCELLED')
        self.message_user(request, f'{updated} competition(s) cancelled.')


@admin.register(CompetitionQuestion)
class CompetitionQuestionAdmin(admin.ModelAdmin):
    list_display = ('competition', 'asked_by', 'is_public', 'answered_at', 'created_at')
    list_filter = ('is_public',)


@admin.register(CompetitionBookmark)
class CompetitionBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'competition', 'created_at')
