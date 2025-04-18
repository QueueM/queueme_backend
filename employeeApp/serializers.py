# File: employeeApp/serializers.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import (
    EmployeeDetailsModel,
    EmployeeWorkingHoursModel,
    EmployeeRoleManangementModel
)
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class EmployeeWorkingHoursSerializer(CustomBaseModelSerializer):
    class Meta:
        model = EmployeeWorkingHoursModel
        exclude = ["employee"]

class EmployeeRoleSerializer(CustomBaseModelSerializer):
    class Meta:
        model = EmployeeRoleManangementModel
        fields = "__all__"

class EmployeeDetailsSerializer(CustomBaseModelSerializer):
    working_hours = EmployeeWorkingHoursSerializer(many=True)
    roles = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeDetailsModel
        fields = "__all__"

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_roles(self, obj):
        """
        Return a list of role objects for this employee.
        """
        roles_qs = obj.roles.all()
        return EmployeeRoleSerializer(roles_qs, many=True).data if roles_qs.exists() else []

    def create(self, validated_data):
        working_hours_data = validated_data.pop('working_hours', [])
        employee = EmployeeDetailsModel.objects.create(**validated_data)
        for hours_data in working_hours_data:
            EmployeeWorkingHoursModel.objects.create(employee=employee, **hours_data)
        return employee

    def update(self, instance, validated_data):
        if 'working_hours' in validated_data:
            working_hours_data = validated_data.pop('working_hours')
            instance.working_hours.all().delete()
            for hours_data in working_hours_data:
                EmployeeWorkingHoursModel.objects.create(employee=instance, **hours_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
