# File: usersapp/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import UserProfileModel
from drf_spectacular.utils import extend_schema_serializer

class UserSerializer(CustomBaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = '__all__'

class UpdateProfileSuggestRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UpdateProfileSuggestResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

@extend_schema_serializer(component_name="UsersAppRegisterUserRequest")
class RegisterUserRequestSerializer(serializers.Serializer):
    name         = serializers.CharField()
    phone_number = serializers.CharField()
    otp          = serializers.CharField()

@extend_schema_serializer(component_name="UsersAppRegisterUserResponse")
class RegisterUserResponseSerializer(serializers.Serializer):
    id           = serializers.IntegerField()
    username     = serializers.CharField()
    name         = serializers.CharField()
    phone_number = serializers.CharField()

class UserMasterDetailsResponseSerializer(serializers.Serializer):
    user                 = UserSerializer()
    customer_details     = serializers.DictField(allow_null=True)
    company_details      = serializers.DictField(allow_null=True)
    employee_details     = serializers.DictField(allow_null=True)
    subscription_details = serializers.DictField(allow_null=True)
