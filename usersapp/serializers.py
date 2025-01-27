

from rest_framework import serializers

from .models import UserProfileModel

class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"