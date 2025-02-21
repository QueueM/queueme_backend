

from rest_framework import serializers
from .models import ShopServiceDetailsModel, ShopServiceCategoryModel, ServiceBookingDetailsModel, ServiceBookingDiscountCouponsModel, ShopServiceTimeSlotModel
from .models import ShopServiceGalleryModel

class ShopServiceTimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopServiceTimeSlotModel
        # fields = '__all__'
        exclude = ["service"]

class ShopServiceDetailsModelSerializer(serializers.ModelSerializer):
    time_slots = ShopServiceTimeSlotSerializer(source='available_time_slots', many=True, read_only=True)
    bookings_count = serializers.SerializerMethodField()
    class Meta:
        model = ShopServiceDetailsModel
        fields = '__all__'

    def get_bookings_count(self, obj):
        return ServiceBookingDetailsModel.objects.filter(service=obj).count()
    
    def create(self, validated_data):
        time_slots_data = self.context['request'].data.get('time_slots', [])
        if "specialists" in self.context['request'].data:
            validated_data.pop("specialists")
        service = ShopServiceDetailsModel.objects.create(**validated_data)
        specialists_data = self.context['request'].data.get('specialists', [])
        
        if specialists_data:
            service.specialists.set(specialists_data)
        else:
            service.specialists.clear()
        
        for slot_data in time_slots_data:
            ShopServiceTimeSlotModel.objects.create(service=service, **slot_data)
        
        return service

    def update(self, instance, validated_data):
        time_slots_data = self.context['request'].data.get('time_slots', [])
        request_data = self.context['request'].data
        for attr, value in validated_data.items():
            if attr != 'specialists':
                setattr(instance, attr, value)
        instance.save()

        # Clear existing time slots and add new ones
        if time_slots_data:
            instance.available_time_slots.all().delete()
            for slot_data in time_slots_data:
                ShopServiceTimeSlotModel.objects.create(service=instance, **slot_data)
        
        if 'specialists' in request_data:
            specialists_data = self.context['request'].data.get('specialists', [])
            instance.specialists.set(specialists_data)  # Use .set() for ManyToMany fields
        
        return instance

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

class ShopServiceGalleryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopServiceGalleryModel
        fields = "__all__"