import django_filters
from .models import Competition


class CompetitionFilter(django_filters.FilterSet):
    """Filter set for Competition model."""
    category = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    budget_min = django_filters.NumberFilter(field_name='budget', lookup_expr='gte')
    budget_max = django_filters.NumberFilter(field_name='budget', lookup_expr='lte')
    deadline_before = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = django_filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')
    tags = django_filters.CharFilter(field_name='tags', lookup_expr='icontains')

    class Meta:
        model = Competition
        fields = ['category', 'status', 'budget_min', 'budget_max',
                  'deadline_before', 'deadline_after', 'tags']
