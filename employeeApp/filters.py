

from django_filters import rest_framework as filters
from .models import EmployeeDetailsModel
from django_filters.rest_framework import CharFilter
from django.db.models import Q
from .models import EmployeeRoleManangementModel
from customClasses.BaseFilterSet import BaseFilterSet

class EmployeeDetailsFilter(BaseFilterSet):
    # group = filters.NumberFilter(field_name='group')
    query = CharFilter(method='filter_query')
    class Meta:
        model = EmployeeDetailsModel
        # fields = ["user"]
        # fields = '__all__'
        exclude = ['avatar_image']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value) | Q(employee_id__icontains=value)
        )

class EmployeeRoleFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    class Meta:
        model = EmployeeRoleManangementModel
        # fields = ["employee", "shop"]
        fields = '__all__'
        
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value) | Q(employee_employee_id__icontains=value) | Q(employee_name__icontains=value)
        )
    