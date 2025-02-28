



from rest_framework import serializers

from .models import CustomersDetailsModel

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CustomersDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersDetailsModel
        fields = "__all__"