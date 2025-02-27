

from django_filters import rest_framework as filters
from .models import ShopServiceGalleryModel, ServiceBookingDetailsModel, ShopServiceDetailsModel
from django_filters.rest_framework import CharFilter
from django.db.models import Q
from customClasses.BaseFilterSet import BaseFilterSet
class ShopServiceGalleryFilter(BaseFilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopServiceGalleryModel
        # fields = ['service']
        fields = "__all__"


class ServiceBookingDetailsFilter(BaseFilterSet):
    # group = filters.NumberFilter(field_name='group')
    query = CharFilter(method='filter_query')
    class Meta:
        model = ServiceBookingDetailsModel
        fields = "__all__"

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(customer__name__icontains=value) | Q(id__icontains=value) | Q(customer__id__icontains=value)
        )

# class ShopServiceDetailsFilter(filters.FilterSet):
#     # group = filters.NumberFilter(field_name='group')
#     query = CharFilter(method='filter_query')
#     class Meta:
#         model = ShopServiceDetailsModel
#         fields = ['shop']
        
#     def filter_query(self, queryset, name, value):
#         return queryset.filter(
#             Q(name__icontains=value) | Q(id__icontains=value)
#         )
    
class ShopServiceDetailsFilter(BaseFilterSet):
    query = filters.CharFilter(method="filter_query")

    class Meta:
        model = ShopServiceDetailsModel
        fields = "__all__"  # Automatically include all fields

    def filter_query(self, queryset, name, value):
        """Custom search filter for name and ID"""
        return queryset.filter(Q(name__icontains=value) | Q(id__icontains=value))