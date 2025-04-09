from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet  # Ensure this is correctly subclassing filters.FilterSet
from django.db import models
from django.db.models import Q

# Models from shopApp
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
)

# DashboardLog is defined in shopDashboardApp.models.
from shopDashboardApp.models import DashboardLog


class ShopGalleryImagesFilter(BaseFilterSet):
    """
    Filter for ShopGalleryImagesModel.
    Allows filtering by the associated shop ID.
    """
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")

    class Meta:
        model = ShopGalleryImagesModel
        exclude = ['image']


class ShopDetailsViewsetFilter(BaseFilterSet):
    """
    Filter for ShopDetailsModel.
    Allows filtering by company ID and free-text search on shop name or shop ID.
    """
    company = filters.NumberFilter(field_name='company__id', help_text="Filter by company ID")
    query = filters.CharFilter(method='filter_query', help_text="Search by shop name or shop ID")

    class Meta:
        model = ShopDetailsModel
        exclude = ['cover_image', 'avatar_image', 'ai_recommendations']
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }

    def filter_query(self, queryset, name, value):
        """
        Filters the queryset by checking if the shop name (case-insensitive)
        contains the query or if the query can be interpreted as a shop ID.
        """
        try:
            id_val = int(value)
            id_filter = Q(id=id_val)
        except (ValueError, TypeError):
            id_filter = Q()
        return queryset.filter(Q(shop_name__icontains=value) | id_filter)


class ShopSpecialistDetailsFilter(BaseFilterSet):
    """
    Filter for ShopSpecialistDetailsModel.
    Allows filtering by shop ID and free-text search on speciality or specialist ID.
    """
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")
    query = filters.CharFilter(method='filter_query', help_text="Search by speciality or specialist ID")

    class Meta:
        model = ShopSpecialistDetailsModel
        exclude = ['avatar_image']

    def filter_query(self, queryset, name, value):
        """
        Filters the queryset by checking if the speciality field (case-insensitive)
        contains the query or if the query can be interpreted as a specialist ID.
        """
        try:
            id_val = int(value)
            id_filter = Q(id=id_val)
        except (ValueError, TypeError):
            id_filter = Q()
        return queryset.filter(Q(speciality__icontains=value) | id_filter)


class DashboardLogFilter(BaseFilterSet):
    """
    Filter for DashboardLog.
    Supports filtering by:
      - A range of timestamps.
      - Company ID and Shop ID.
      - Numeric filtering on total_bookings and total_revenue.
    """
    timestamp = filters.DateFromToRangeFilter()
    company = filters.NumberFilter(field_name='company__id', help_text="Filter by company ID")
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")
    total_bookings = filters.NumberFilter()
    total_revenue = filters.NumberFilter()

    class Meta:
        model = DashboardLog
        fields = ['timestamp', 'company', 'shop', 'total_bookings', 'total_revenue']
