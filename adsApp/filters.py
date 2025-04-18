from django.db import models
from django_filters import rest_framework as filters
from customClasses.BaseFilterSet import BaseFilterSet
from .models import ShopAdsModel, ShopAdsImpressionModel

class ShopAdsFilter(BaseFilterSet):
    class Meta:
        model = ShopAdsModel
        fields = '__all__'
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'},
            },
        }

class ShopAdsImpressionFilter(BaseFilterSet):
    class Meta:
        model = ShopAdsImpressionModel
        fields = '__all__'
