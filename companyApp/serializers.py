

from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from .models import CompanyDetailsModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class CompanyDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = CompanyDetailsModel
        fields = "__all__"
        read_only_fields = ['user']

    def validate(self, data):
        data['user'] = self.context['user'] 
        if CompanyDetailsModel.objects.filter(user=self.context['user']):
            raise ValidationError("User already have a company registered")
        return data
