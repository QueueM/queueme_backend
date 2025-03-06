

from rest_framework import serializers
from .models import ShopAdsModel, ShopAdsImpressionModel

class ShopAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdsModel
        fields = "__all__"

class ShopAdsImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopAdsImpressionModel
        fields = "__all__"