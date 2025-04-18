import django_filters
from django.db import models
from .models import ReelsModel, CommentsModel

class ReelsFilter(django_filters.FilterSet):
    created_at_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_at_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = ReelsModel
        fields = {
            'shop': ['exact'],
            'view_count': ['gte', 'lte'],
        }

class CommentsFilter(django_filters.FilterSet):
    created_at_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_at_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = CommentsModel
        fields = {
            'user': ['exact'],
            'reel': ['exact'],
        }
