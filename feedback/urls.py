from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('reviews/', views.CreateReviewView.as_view(), name='create-review'),
    path('users/<uuid:user_id>/reviews/', views.UserReviewsView.as_view(), name='user-reviews'),
    path('competitions/<uuid:competition_id>/reviews/', views.CompetitionReviewsView.as_view(), name='competition-reviews'),
]
