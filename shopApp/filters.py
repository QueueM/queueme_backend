# shopApp/filters.py
from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet  # Ensure this properly subclasses django_filters.FilterSet
from django.db import models
from django.db.models import Q
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
)
# If needed, import DashboardLog model from shopDashboardApp
from shopDashboardApp.models import DashboardLog

class ShopGalleryImagesFilter(BaseFilterSet):
    """
    Filter for ShopGalleryImagesModel by shop ID.
    """
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")

    class Meta:
        model = ShopGalleryImagesModel
        exclude = ['image']

class ShopDetailsViewsetFilter(BaseFilterSet):
    """
    Filter for ShopDetailsModel.
    Supports filtering by company ID and free-text search on shop name or shop ID.
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
        try:
            id_val = int(value)
            id_filter = Q(id=id_val)
        except (ValueError, TypeError):
            id_filter = Q()
        return queryset.filter(Q(shop_name__icontains=value) | id_filter)

class ShopSpecialistDetailsFilter(BaseFilterSet):
    """
    Filter for ShopSpecialistDetailsModel.
    Supports filtering by shop ID and free-text search on speciality or specialist ID.
    """
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")
    query = filters.CharFilter(method='filter_query', help_text="Search by speciality or specialist ID")

    class Meta:
        model = ShopSpecialistDetailsModel
        exclude = ['avatar_image']

    def filter_query(self, queryset, name, value):
        try:
            id_val = int(value)
            id_filter = Q(id=id_val)
        except (ValueError, TypeError):
            id_filter = Q()
        return queryset.filter(Q(speciality__icontains=value) | id_filter)

class DashboardLogFilter(BaseFilterSet):
    """
    Filter for DashboardLog for timestamp range, company, shop, and numerical fields.
    """
    timestamp = filters.DateFromToRangeFilter()
    company = filters.NumberFilter(field_name='company__id', help_text="Filter by company ID")
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")
    total_bookings = filters.NumberFilter()
    total_revenue = filters.NumberFilter()

    class Meta:
        model = DashboardLog
        fields = ['timestamp', 'company', 'shop', 'total_bookings', 'total_revenue']
