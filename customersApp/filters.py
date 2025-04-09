

from django_filters import rest_framework as filters
from .models import CustomersDetailsModel
from django_filters.rest_framework import CharFilter
from django.db.models import Q
from customClasses.BaseFilterSet import BaseFilterSet
class CustomerDetailsViewsetFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    class Meta:
        model = CustomersDetailsModel
        # fields = ['gender','customer_type','preferred_services']
        # fields = '__all__'
        exclude = ['profie_photo']
        
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value)
        )
        