


from rest_framework import serializers

from .models import ShopDetailsModel, ShopPermissionsModel, ShopGalleryImagesModel, ShopSpecialistDetailsModel
from companyApp.models import CompanyDetailsModel
from rest_framework.exceptions import ValidationError
class ShopDetailsModelSerializer(serializers.ModelSerializer):
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