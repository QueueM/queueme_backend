# shopApp/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import (
    ShopDetailsModel, 
    ShopPermissionsModel, 
    ShopGalleryImagesModel, 
    ShopSpecialistDetailsModel, 
    ShopOpeningHoursModel,
    SpecialistTypesModel
)
from companyApp.models import CompanyDetailsModel
from shopServiceApp.models import ShopServiceCategoryModel
from employeeApp.models import EmployeeDetailsModel

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
        queryset=ShopServiceCategoryModel.objects.all(), many=True
    )
    opening_hours = ShopOpeningHoursModelSerializer(many=True)
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ShopDetailsModel
        fields = "__all__"
        read_only_fields = ['owner', 'company', 'ai_recommendations', 'ai_personalization']
    
    def get_employee_count(self, obj):
        return EmployeeDetailsModel.objects.filter(shop=obj).count()
    
    def validate(self, data):
        user = self.context.get('user')
        if user and CompanyDetailsModel.objects.filter(user=user).exists():
            data['company'] = CompanyDetailsModel.objects.get(user=user)
            data['owner'] = user
            return data
        else:
            raise ValidationError('User account is not registered as company!')
    
    def create(self, validated_data):
        if ShopDetailsModel.objects.filter(shop_name=validated_data.get('shop_name')).exists():
            raise ValidationError('Shop name must be unique.')
        
        categories_data = validated_data.pop('categories', [])
        opening_hours_data = validated_data.pop('opening_hours', [])

        shop = ShopDetailsModel.objects.create(**validated_data)
        shop.categories.set(categories_data)

        for hours_data in opening_hours_data:
            ShopOpeningHoursModel.objects.create(shop=shop, **hours_data)
        
        # AI fields will be updated via the post_save signal.
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

class ShopPermissionsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopPermissionsModel
        fields = "__all__"
    
class ShopGalleryImagesModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopGalleryImagesModel
        fields = "__all__"

class ShopSpecialistDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopSpecialistDetailsModel
        fields = "__all__"
