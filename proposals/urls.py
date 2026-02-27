from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('submit/', views.ProposalCreateView.as_view(), name='proposal-create'),
    path('mine/', views.MyProposalsView.as_view(), name='my-proposals'),
    path('<uuid:proposal_id>/', views.ProposalDetailView.as_view(), name='proposal-detail'),
    path('<uuid:proposal_id>/attachments/', views.AddAttachmentView.as_view(), name='add-attachment'),
    path('<uuid:proposal_id>/attachments/<uuid:attachment_id>/', views.DeleteAttachmentView.as_view(), name='delete-attachment'),
    path('competition/<uuid:competition_id>/', views.CompetitionProposalsView.as_view(), name='competition-proposals'),
    path('<uuid:proposal_id>/score/', views.ScoreProposalView.as_view(), name='score-proposal'),
    path('<uuid:proposal_id>/withdraw/', views.WithdrawProposalView.as_view(), name='withdraw-proposal'),
]
