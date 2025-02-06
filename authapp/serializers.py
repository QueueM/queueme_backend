


from rest_framework import serializers

from .models import SendOTPModel
from django.contrib.auth.models import User
class SendOTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendOTPModel
        fields = "__all__"
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    phone_no = serializers.CharField(write_only=True, min_length=10) 
    class Meta:
        model = User
        fields = ['password', 'phone_no']

    def validate(self, data):
        data['username'] = 'phone_no'
        return data

    def create(self, validated_data):
        validated_data.pop('phone_no')  # Remove confirm_password
        user = User.objects.create_user(**validated_data)
        return user
