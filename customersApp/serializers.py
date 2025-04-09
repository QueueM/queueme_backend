



from rest_framework import serializers

from .models import CustomersDetailsModel

from django.contrib.auth.models import User
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class UserSerializer(CustomBaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomersDetailsModelSerializer(CustomBaseModelSerializer):
    class Meta:
        model = CustomersDetailsModel
        fields = "__all__"