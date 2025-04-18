# File: shopApp/serializers.py

from rest_framework import serializers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import ShopDetailsModel, ShopSpecialistDetailsModel, ShopGalleryImagesModel, SpecialistTypesModel

class ShopDetailsModelSerializer(CustomBaseModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = ShopDetailsModel
        fields = '__all__'

    # declare return type for spectacular
    @extend_schema_field(OpenApiTypes.INT)
    def get_employee_count(self, obj) -> int:
        return obj.employees.count()

class ShopGalleryImagesModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopGalleryImagesModel
        fields = '__all__'

class ShopSpecialistDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ShopSpecialistDetailsModel
        fields = '__all__'

class SpecialistTypesSerializer(CustomBaseModelSerializer):
    class Meta:
        model = SpecialistTypesModel
        fields = '__all__'
