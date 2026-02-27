from django.urls import path
from . import views

app_name = 'competitions'

urlpatterns = [
    path('', views.CompetitionListView.as_view(), name='competition-list'),
    path('create/', views.CompetitionCreateView.as_view(), name='competition-create'),
    path('mine/', views.MyCompetitionsView.as_view(), name='my-competitions'),
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark-list'),
    path('<uuid:competition_id>/', views.CompetitionDetailView.as_view(), name='competition-detail'),
    path('<uuid:competition_id>/status/', views.CompetitionStatusView.as_view(), name='competition-status'),
    path('<uuid:competition_id>/questions/', views.CompetitionQuestionListCreateView.as_view(), name='competition-questions'),
    path('<uuid:competition_id>/questions/<uuid:question_id>/answer/', views.CompetitionAnswerView.as_view(), name='competition-answer'),
    path('<uuid:competition_id>/bookmark/', views.CompetitionBookmarkView.as_view(), name='competition-bookmark'),
    path('<uuid:competition_id>/select-winner/', views.SelectWinnerView.as_view(), name='select-winner'),
]
