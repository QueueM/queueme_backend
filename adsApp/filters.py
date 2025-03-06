

from customClasses.BaseFilterSet import BaseFilterSet
from .models import ShopAdsModel, ShopAdsImpressionModel

class ShopAdsFilter(BaseFilterSet):

    class Meta:
        model = ShopAdsModel
        fields = '__all__'

class ShopAdsImpressionFilter(BaseFilterSet):

    class Meta:
        model = ShopAdsImpressionModel
        fields = '__all__'