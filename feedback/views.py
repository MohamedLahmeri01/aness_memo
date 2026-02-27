from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from freelance_arena.utils import success_response
from .models import Review, UserRating
from .serializers import (
    ReviewCreateSerializer,
    ReviewDetailSerializer,
    UserRatingSerializer,
)


class CreateReviewView(APIView):
    """POST - Create a review. Authenticated users only, after competition closes."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return success_response(
            data=ReviewDetailSerializer(review).data,
            message='Review submitted successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class UserReviewsView(generics.ListAPIView):
    """GET - Public reviews for a specific user."""
    serializer_class = ReviewDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(reviewee_id=user_id, is_public=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Also include user rating summary
        user_id = self.kwargs['user_id']
        try:
            rating = UserRating.objects.get(user_id=user_id)
            rating_data = UserRatingSerializer(rating).data
        except UserRating.DoesNotExist:
            rating_data = {'average_rating': 0, 'total_reviews': 0}

        return success_response(
            data={
                'reviews': response.data,
                'rating_summary': rating_data,
            },
            message='User reviews retrieved.',
        )


class CompetitionReviewsView(generics.ListAPIView):
    """GET - Reviews for a specific competition. Authenticated."""
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        competition_id = self.kwargs['competition_id']
        return Review.objects.filter(competition_id=competition_id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(data=response.data, message='Competition reviews retrieved.')
