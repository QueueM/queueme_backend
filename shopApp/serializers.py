


from rest_framework import serializers

from .models import ShopDetailsModel, ShopPermissionsModel, ShopGalleryImagesModel, ShopSpecialistDetailsModel, ShopOpeningHoursModel
from companyApp.models import CompanyDetailsModel
from rest_framework.exceptions import ValidationError
from shopServiceApp.serializers import ShopServiceCategoryModelSerializer
from shopServiceApp.models import ShopServiceCategoryModel

class ShopOpeningHoursModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOpeningHoursModel
        fields = "__all__"
class ShopDetailsModelSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=ShopServiceCategoryModel.objects.all(),many=True
        )
    opening_hours = ShopOpeningHoursModelSerializer(many=True)
    class Meta:
        model = ShopDetailsModel
        fields = "__all__"
        read_only_fields = ['owner','company']
    def validate(self, data):
        if self.context['user'] and CompanyDetailsModel.objects.filter(user=self.context['user']).exists():
            data['company'] = CompanyDetailsModel.objects.get(user=self.context['user'])
            data['owner'] = self.context['user']
            return data
        else:
            raise ValidationError('User account is not registerd as company!')
        return data
    
    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        opening_hours_data = validated_data.pop('opening_hours', [])

        shop = ShopDetailsModel.objects.create(**validated_data)

        shop.categories.set(categories_data)

        for hours_data in opening_hours_data:
            ShopOpeningHoursModel.objects.create(shop=shop, **hours_data)
        
        return shop
    
    def update(self, instance, validated_data):
        # Handle category update
        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories', [])
            instance.categories.set(categories_data)  # Update categories

        # Handle opening hours update
        if 'opening_hours' in validated_data:
            opening_hours_data = validated_data.pop('opening_hours')

            # Delete old opening hours
            instance.opening_hours.all().delete()

            # Add new opening hours
            for hours_data in opening_hours_data:
                ShopOpeningHoursModel.objects.create(shop=instance, **hours_data)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class ShopPermissionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopDetailsModel
        fields = "__all__"
    
class ShopGalleryImagesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopGalleryImagesModel
        fields = "__all__"

class ShopSpecialistDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSpecialistDetailsModel
        fields = "__all__"