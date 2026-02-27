from django.contrib import admin
from .models import Review, UserRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'reviewer', 'reviewee', 'competition', 'rating',
        'review_type', 'is_public', 'created_at',
    )
    list_filter = ('review_type', 'is_public', 'rating')
    search_fields = ('comment',)


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'average_rating', 'total_reviews', 'updated_at')
