from django.contrib import admin
from .models import Proposal, ProposalAttachment, ProposalRevision


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'competition', 'freelancer', 'status',
        'proposed_budget', 'client_score', 'created_at',
    )
    list_filter = ('status',)
    search_fields = ('title', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(ProposalAttachment)
class ProposalAttachmentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'proposal', 'file_size', 'file_type', 'uploaded_at')


@admin.register(ProposalRevision)
class ProposalRevisionAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'revised_by', 'revision_number', 'created_at')
