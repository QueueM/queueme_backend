

from rest_framework import serializers
from .models import ShopAdsModel, ShopAdsImpressionModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class ShopAdsSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopAdsModel
        fields = "__all__"

class ShopAdsImpressionSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopAdsImpressionModel
        fields = "__all__"