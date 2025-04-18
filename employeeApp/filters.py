from django.db import models
from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from .models import EmployeeDetailsModel, EmployeeRoleManangementModel
from django_filters.rest_framework import CharFilter
from django.db.models import Q

class EmployeeDetailsFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    
    class Meta:
        model = EmployeeDetailsModel
        exclude = ['avatar_image']
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(id__icontains=value) |
            Q(employee_id__icontains=value)
        )

class EmployeeRoleFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    
    class Meta:
        model = EmployeeRoleManangementModel
        fields = '__all__'
        # If your role model has any JSONField that requires special handling,
        # you can add a filter_overrides entry here as well.
        # For example:
        # filter_overrides = {
        #     models.JSONField: {
        #         'filter_class': filters.CharFilter,
        #         'extra': lambda f: {'lookup_expr': 'icontains'},
        #     },
        # }

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(id__icontains=value) |
            Q(employees__employee_id__icontains=value)
        )
