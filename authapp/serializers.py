


from rest_framework import serializers

from .models import SendOTPModel
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class SendOTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendOTPModel
        fields = "__all__"
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    phone_no = serializers.CharField(write_only=True, min_length=10) 
    otp = serializers.CharField(write_only=True, min_length=4) 
    class Meta:
        model = User
        fields = ['password', 'phone_no', 'otp']

    def validate(self, data):
        data['username'] = data['phone_no']
        otp = data['otp']
        phone_number = data['phone_no']
        otpRecord = SendOTPModel.objects.filter(phone_number=phone_number, otp=otp)
        if not otpRecord.exists():
            raise ValidationError("Invalid OTP!")
        otpRecord.delete()
        return data

    def create(self, validated_data):
        validated_data.pop('phone_no')  # Remove confirm_password
        validated_data.pop('otp')  # Remove confirm_password
        user = User.objects.create_user(**validated_data)
        return user
