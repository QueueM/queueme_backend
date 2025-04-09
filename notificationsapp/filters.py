

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.db.models import Q
from customClasses.BaseFilterSet import BaseFilterSet
from .models import NotificationModel


class NotificationFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    class Meta:
        model = NotificationModel
        fields = '__all__'
    
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            # name__icontains=value
            # Q(name__icontains=value) | Q(id__icontains=value)
            Q(title__icontains=value) | Q(message__icontains=value)
        )


