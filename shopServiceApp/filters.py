# shopServiceApp/filters.py
from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from django.db.models import Q
from django.db import models
from .models import (
    ShopServiceGalleryModel,
    ServiceBookingDetailsModel,
    ShopServiceDetailsModel,
    ShopServiceCategoryModel
)

class ShopServiceGalleryFilter(BaseFilterSet):
    service = filters.ModelChoiceFilter(
        field_name='service',
        queryset=ShopServiceDetailsModel.objects.all()
    )
    class Meta:
        model = ShopServiceGalleryModel
        fields = ['service']

class ServiceBookingDetailsFilter(BaseFilterSet):
    status = filters.ChoiceFilter(field_name='status')
    fraud_flag = filters.BooleanFilter(field_name='fraud_flag')
    booking_date = filters.DateFromToRangeFilter(field_name='booking_date')
    query = filters.CharFilter(method='filter_query')
    class Meta:
        model = ServiceBookingDetailsModel
        exclude = ['created_at']

    def filter_query(self, queryset, name, value):
        return queryset.filter(Q(customer__name__icontains=value) | Q(id__icontains=value))

class ShopServiceDetailsFilter(BaseFilterSet):
    shop = filters.ModelChoiceFilter(
        field_name='shop',
        queryset=ShopServiceDetailsModel.objects.none()
    )
    category = filters.ModelChoiceFilter(
        field_name='category',
        queryset=ShopServiceCategoryModel.objects.all()
    )
    query = filters.CharFilter(method='filter_query')
    class Meta:
        model = ShopServiceDetailsModel
        exclude = ['forecast_data', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['shop'].queryset = ShopServiceDetailsModel.objects.values_list('shop', flat=True).distinct()

    def filter_query(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(id__icontains=value))

class ShopServiceCategoryFilter(BaseFilterSet):
    query = filters.CharFilter(method='filter_query')
    class Meta:
        model = ShopServiceCategoryModel
        fields = "__all__"
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'exact'},
            },
        }
    def filter_query(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(id__icontains=value))
