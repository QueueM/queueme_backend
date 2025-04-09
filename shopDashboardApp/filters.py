from django_filters import rest_framework as filters
from .models import DashboardLog

class DashboardLogFilter(filters.FilterSet):
    company    = filters.NumberFilter(field_name='company_id')
    shop       = filters.NumberFilter(field_name='shop_id')
    date_from  = filters.DateFilter(field_name='timestamp', lookup_expr='date__gte')
    date_to    = filters.DateFilter(field_name='timestamp', lookup_expr='date__lte')

    class Meta:
        model = DashboardLog
        fields = ['company', 'shop', 'date_from', 'date_to']