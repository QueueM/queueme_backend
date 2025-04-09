from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CompanyDetailsModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class CompanyDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = CompanyDetailsModel
        fields = '__all__'
        read_only_fields = ['user', 'forecast_data', 'fraud_flag', 'created_at']

    def validate(self, data):
        # Ensure each user has only one company
        if CompanyDetailsModel.objects.filter(user=self.context['user']).exists():
            raise ValidationError('User already has a registered company')
        data['user'] = self.context['user']
        return data
