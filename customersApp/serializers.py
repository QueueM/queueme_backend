from rest_framework import serializers
from .models import CustomersDetailsModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class CustomersDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = CustomersDetailsModel
        fields = "__all__"
