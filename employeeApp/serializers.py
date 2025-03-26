from rest_framework import serializers

from .models import EmployeeDetailsModel, EmployeeWorkingHoursModel

from shopApp.models import ShopDetailsModel
from .models import EmployeeRoleManangementModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class EmployeeWorkingHoursSerializer(CustomBaseModelSerializer):
    
    class Meta:
        model = EmployeeWorkingHoursModel
        # fields = "__all__"
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

    def validate(self, data):
        return data
    
    def get_roles(self, obj):
        """Return a list of roles or an empty list if none exist."""
        roles = obj.roles.all()  # Fetch related roles using related_name="role"
        return EmployeeRoleSerializer(roles, many=True).data if roles.exists() else []
    def create(self, validated_data):
        opening_hours_data = validated_data.pop('working_hours', [])
        employee = EmployeeDetailsModel.objects.create(**validated_data)
        for hours_data in opening_hours_data:
            EmployeeWorkingHoursModel.objects.create(employee=employee, **hours_data)
        
        return employee
    
    def update(self, instance, validated_data):
        # Handle working hours update
        if 'working_hours' in validated_data:
            opening_hours_data = validated_data.pop('working_hours')

            # Delete old opening hours
            instance.working_hours.all().delete()

            # Add new opening hours
            for hours_data in opening_hours_data:
                EmployeeWorkingHoursModel.objects.create(employee=instance, **hours_data)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



    