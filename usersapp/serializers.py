

from rest_framework import serializers

from .models import UserProfileModel
from django.contrib.auth.models import User
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class UserSerializer(CustomBaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserProfileModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"