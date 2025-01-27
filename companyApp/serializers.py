

from rest_framework import serializers

from .models import CompanyDetailsModel, CompanyEmployeeDetailsModel, CompanyEmployeeRoleManagementModel



class CompanyDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetailsModel
        fields = "__all__"

class CompanyEmployeeDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEmployeeDetailsModel
        fields = "__all__"

class CompanyEmployeeRoleManagementModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyEmployeeRoleManagementModel
        fields = "__all__"