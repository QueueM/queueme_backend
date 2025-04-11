# companyApp/serializers.py
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import CompanyDetailsModel

class CompanyDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = CompanyDetailsModel
        fields = '__all__'
        read_only_fields = ['user', 'forecast_data', 'fraud_flag', 'created_at']
        # You can decide whether online_payment_global_enabled is editable or not.

    def validate(self, data):
        user = self.context.get('user')
        if CompanyDetailsModel.objects.filter(user=user).exists():
            raise ValidationError('User already has a registered company')
        data['user'] = user
        return data
