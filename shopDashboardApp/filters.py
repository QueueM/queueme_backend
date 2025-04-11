from django_filters import rest_framework as filters
from .models import DashboardLog

class DashboardLogFilter(filters.FilterSet):
    # Use query parameters 'companyid' and 'shopid' to filter by the respective foreign keys.
    companyid = filters.NumberFilter(field_name='company_id')
    shopid = filters.NumberFilter(field_name='shop_id')
    # For date filtering on the timestamp field (using the full datetime):
    date_from = filters.DateFilter(field_name='timestamp', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='timestamp', lookup_expr='lte')

    class Meta:
        model = DashboardLog
        fields = ['companyid', 'shopid', 'date_from', 'date_to']
