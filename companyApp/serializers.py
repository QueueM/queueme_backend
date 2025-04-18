# File: companyApp/serializers.py

from rest_framework import serializers
from .models import CompanyDetailsModel

class CompanyDetailsModelSerializer(serializers.ModelSerializer):
    """
    Serializer for CompanyDetailsModel instances.
    """
    class Meta:
        model = CompanyDetailsModel
        fields = [
            'user', 'name', 'company_image', 'description', 'address',
            'is_verified', 'status', 'shops_limit', 'merchant_type',
            'name_arabic', 'registration_document', 'tax_number',
            'online_payment_global_enabled', 'forecast_data', 'fraud_flag',
            'created_at'
        ]

class RegisterCompanyRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=300)
    description = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    merchant_type = serializers.ChoiceField(choices=CompanyDetailsModel.MERCHANT_TYPE.choices)

class RegisterCompanyResponseSerializer(serializers.Serializer):
    company = CompanyDetailsModelSerializer()
