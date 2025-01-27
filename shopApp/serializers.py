


from rest_framework import serializers

from .models import ShopDetailsModel, ShopPermissionsModel, ShopGalleryImagesModel, ShopSpecialistDetailsModel

class ShopDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopDetailsModel
        fields = "__all__"
        
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