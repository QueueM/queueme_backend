# shopServiceApp/serializers.py
from rest_framework import serializers
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from ai_features.fraud_detection import check_booking

from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceTimeSlotModel,
    ShopServiceGalleryModel
)

class ShopServiceTimeSlotSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopServiceTimeSlotModel
        exclude = ['service']

class ShopServiceCategoryModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopServiceCategoryModel
        fields = '__all__'
        read_only_fields = ['created_at', 'forecast_data']

class ShopServiceDetailsModelSerializer(CustomBaseModelSerializer):
    time_slots = ShopServiceTimeSlotSerializer(
        source='available_time_slots', many=True, read_only=True
    )
    bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = ShopServiceDetailsModel
        fields = '__all__'
        read_only_fields = ['created_at', 'forecast_data', 'bookings_count']

    def get_bookings_count(self, obj):
        return obj.bookings.count()

class ServiceBookingDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceBookingDetailsModel
        fields = '__all__'
        read_only_fields = ['created_at', 'fraud_flag', 'price', 'final_amount', 'user']

    def validate(self, data):
        # Assign the current user automatically
        data['user'] = self.context['request'].user
        return data

    def create(self, validated_data):
        booking = super().create(validated_data)
        # AI-based fraud detection
        try:
            is_fraud = check_booking(booking)
            booking.fraud_flag = is_fraud
            booking.save(update_fields=['fraud_flag'])
        except Exception:
            # Optionally log the error
            pass
        return booking

class ServiceBookingDiscountCouponsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceBookingDiscountCouponsModel
        fields = '__all__'

class ShopServiceGalleryModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopServiceGalleryModel
        fields = '__all__'
