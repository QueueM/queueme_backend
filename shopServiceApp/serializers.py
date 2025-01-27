

from rest_framework import serializers
from .models import ShopServiceDetailsModel, ShopServiceCategoryModel, ServiceBookingDetailsModel, ServiceBookingDiscountCouponsModel


class ShopServiceDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopServiceDetailsModel
        fields = "__all__"

class ShopServiceCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopServiceCategoryModel
        fields = "__all__"

class ServiceBookingDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBookingDetailsModel
        fields = "__all__"
        read_only_fields = ['final_amount','user']

    def validate(self, data):
        data['user'] = self.context['user']
        return data

class ServiceBookingDiscountCouponsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBookingDiscountCouponsModel
        fields = "__all__"