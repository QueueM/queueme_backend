

from rest_framework import serializers

from .models import CompanyDetailsModel, CompanyEmployeeDetailsModel, CompanyEmployeeRoleManagementModel
from rest_framework.exceptions import ValidationError


class CompanyDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetailsModel
        fields = "__all__"
        read_only_fields = ['user']

    def validate(self, data):
        data['user'] = self.context['user'] 
        if CompanyDetailsModel.objects.filter(user=self.context['user']):
            raise ValidationError("User already have a company registered")
        return data

class CompanyEmployeeDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEmployeeDetailsModel
        fields = "__all__"

class CompanyEmployeeRoleManagementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEmployeeRoleManagementModel
        fields = "__all__"