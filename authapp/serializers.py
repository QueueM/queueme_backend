# File: authapp/serializers.py

from rest_framework import serializers

class RegistrationOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp_type = serializers.CharField()

class RegistrationOTPResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    # only in dev
    otp = serializers.CharField(required=False)

class TestResponseSerializer(serializers.Serializer):
    name = serializers.CharField()

class RegisterUserRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    otp = serializers.CharField()

class RegisterUserResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()
    access = serializers.CharField()
    refresh = serializers.CharField()

class LoginWithOTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

class LoginWithOTPResponseSerializer(serializers.Serializer):
    user_details = serializers.DictField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    customer_details = serializers.DictField(allow_null=True)
    company_details = serializers.DictField(allow_null=True)
    employee_details = serializers.DictField(allow_null=True)

class UnifiedLoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()

class UnifiedLoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    roles = serializers.ListField(child=serializers.CharField())
