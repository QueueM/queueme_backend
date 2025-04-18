from rest_framework import serializers
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import ShopAdsModel, ShopAdsImpressionModel

class ShopAdsSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopAdsModel
        fields = "__all__"

class ShopAdsImpressionSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopAdsImpressionModel
        fields = "__all__"
