

from django_filters import rest_framework as filters
from .models import EmployeeDetailsModel
from django_filters.rest_framework import CharFilter
from django.db.models import Q



class EmployeeDetailsFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')
    query = CharFilter(method='filter_query')
    class Meta:
        model = EmployeeDetailsModel
        fields = ["user"]

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value) | Q(employee_id__icontains=value)
        )