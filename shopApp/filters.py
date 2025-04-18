from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from django.db import models
from django.db.models import Q
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
)
# Optionally import DashboardLog from shopDashboardApp if required.
from shopDashboardApp.models import DashboardLog

class ShopGalleryImagesFilter(BaseFilterSet):
    shop = filters.NumberFilter(field_name='shop__id', help_text="Filter by shop ID")

    class Meta:
        model = ShopGalleryImagesModel
        exclude = ['image']

class ShopDetailsViewsetFilter(BaseFilterSet):
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
