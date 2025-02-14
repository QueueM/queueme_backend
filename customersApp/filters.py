

from django_filters import rest_framework as filters
from .models import CustomersDetailsModel

class CustomerDetailsViewsetFilter(filters.FilterSet):
    class Meta:
        model = CustomersDetailsModel
        fields = ['gender','customer_type','preferred_services']
        