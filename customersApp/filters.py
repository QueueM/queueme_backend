from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from django_filters.rest_framework import CharFilter
from django.db.models import Q
from .models import CustomersDetailsModel

class CustomerDetailsViewsetFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    class Meta:
        model = CustomersDetailsModel
        # Exclude image field if not needed.
        exclude = ['profie_photo']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value)
        )
