# File: shopServiceApp/serializers.py

import re
from datetime import timedelta
from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceExtendedDetailsModel,
    ServiceOverview,
    ServiceFAQ,
    ServiceProcessStep,
    ServiceBenefit,
    ServiceAftercareTip,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceTimeSlotModel,
    ShopServiceGalleryModel,
)

# Mark this custom field as a string in the OpenAPI schema
@extend_schema_field(OpenApiTypes.STR)
class DurationField(serializers.Field):
    def to_internal_value(self, data):
        if isinstance(data, str):
            pattern = r'^(\d{2}):(\d{2}):(\d{2})$'
            match = re.match(pattern, data)
            if not match:
                raise serializers.ValidationError("Duration must be in the format HH:MM:SS.")
            hours, minutes, seconds = map(int, match.groups())
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        elif isinstance(data, timedelta):
            return data
        else:
            raise serializers.ValidationError("Invalid duration format; expected HH:MM:SS string.")

    def to_representation(self, value):
        if not isinstance(value, timedelta):
            return value
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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
    time_slots = ShopServiceTimeSlotSerializer(source='available_time_slots', many=True, read_only=True)
    bookings_count = serializers.SerializerMethodField()
    duration = DurationField()

    class Meta:
        model = ShopServiceDetailsModel
        fields = '__all__'
        read_only_fields = ['created_at', 'forecast_data', 'bookings_count']

    # tell spectacular this returns an integer
    @extend_schema_field(OpenApiTypes.INT)
    def get_bookings_count(self, obj) -> int:
        return obj.bookings.count()

class ServiceOverviewSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceOverview
        fields = '__all__'

class ServiceFAQSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = '__all__'

class ServiceProcessStepSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceProcessStep
        fields = '__all__'

class ServiceBenefitSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceBenefit
        fields = '__all__'

class ServiceAftercareTipSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceAftercareTip
        fields = '__all__'

class ServiceExtendedDetailsModelSerializer(CustomBaseModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    overviews = ServiceOverviewSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    process_steps = ServiceProcessStepSerializer(many=True, read_only=True)
    benefits = ServiceBenefitSerializer(many=True, read_only=True)
    aftercare_tips = ServiceAftercareTipSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceExtendedDetailsModel
        fields = '__all__'

class ServiceBookingDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ServiceBookingDetailsModel
        fields = '__all__'
        read_only_fields = ['created_at', 'fraud_flag', 'price', 'final_amount', 'user']

    def validate(self, data):
        data['user'] = self.context['request'].user
        return data

    def create(self, validated_data):
        booking = super().create(validated_data)
        try:
            from ai_features.fraud_detection import check_booking
            booking.fraud_flag = check_booking(booking)
            booking.save(update_fields=['fraud_flag'])
        except Exception:
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
