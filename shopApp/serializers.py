# shopApp/serializers.py
from rest_framework import serializers
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    ShopOpeningHoursModel,
    SpecialistTypesModel,
)
from shopServiceApp.models import ShopServiceCategoryModel

class ShopOpeningHoursModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopOpeningHoursModel
        exclude = ["shop"]

class SpecialistTypesSerializer(CustomBaseModelSerializer):
    class Meta:
        model = SpecialistTypesModel
        fields = "__all__"

class ShopDetailsModelSerializer(CustomBaseModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=ShopServiceCategoryModel.objects.all(),
        many=True
    )
    opening_hours = ShopOpeningHoursModelSerializer(many=True)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = ShopDetailsModel
        fields = "__all__"
        read_only_fields = ['owner', 'company', 'ai_recommendations', 'ai_personalization', 'created_at']

    def get_employee_count(self, obj):
        from employeeApp.models import EmployeeDetailsModel
        return EmployeeDetailsModel.objects.filter(shop=obj).count()

    def validate(self, data):
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User is required.")
        data['owner'] = user
        # If online_payment_requested is True, bank_details_document must be provided.
        if data.get('online_payment_requested', False) and not data.get('bank_details_document'):
            raise serializers.ValidationError("Bank details document is required when requesting online payments.")
        return data

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        opening_hours_data = validated_data.pop('opening_hours', [])
        shop = ShopDetailsModel.objects.create(**validated_data)
        if categories_data:
            shop.categories.set(categories_data)
        for hours_data in opening_hours_data:
            ShopOpeningHoursModel.objects.create(shop=shop, **hours_data)
        return shop

    def update(self, instance, validated_data):
        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories', [])
            instance.categories.set(categories_data)
        if 'opening_hours' in validated_data:
            opening_hours_data = validated_data.pop('opening_hours')
            instance.opening_hours.all().delete()
            for hours_data in opening_hours_data:
                ShopOpeningHoursModel.objects.create(shop=instance, **hours_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class ShopGalleryImagesModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopGalleryImagesModel
        fields = "__all__"

class ShopSpecialistDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopSpecialistDetailsModel
        fields = "__all__"
