from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from .models import CompanyDetailsModel

class CompanyDetailsFilter(BaseFilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    contact_email = filters.CharFilter(field_name='contact_email', lookup_expr='icontains')

    class Meta:
        model = CompanyDetailsModel
        fields = ['name', 'contact_email']
