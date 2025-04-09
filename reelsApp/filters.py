from django.db import models
from customClasses.BaseFilterSet import BaseFilterSet
from .models import ReelsModel, CommentsModel, StoryModel
from django_filters import rest_framework as filters

class ReelsFilter(BaseFilterSet):
    class Meta:
        model = ReelsModel
        fields = '__all__'
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }

class ReelsCommentsFilter(BaseFilterSet):
    class Meta:
        model = CommentsModel
        fields = '__all__'

class StoryFilter(BaseFilterSet):
    class Meta:
        model = StoryModel
        fields = '__all__'
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }
