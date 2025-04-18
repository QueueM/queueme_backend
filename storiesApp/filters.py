from django_filters import rest_framework as filters
from django.db import models
from .models import StoryModel

class StoryFilter(filters.FilterSet):
    class Meta:
        model = StoryModel
        fields = '__all__'
        filter_overrides = {
            models.FileField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }
