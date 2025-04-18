from django_filters import rest_framework as filters
from .models import DashboardLog

class DashboardLogFilter(filters.FilterSet):
    companyid = filters.NumberFilter(field_name='company_id')
    shopid = filters.NumberFilter(field_name='shop_id')
    date_from = filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = DashboardLog
        fields = ['companyid', 'shopid', 'date_from', 'date_to']
