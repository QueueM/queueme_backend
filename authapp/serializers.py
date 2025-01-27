


from rest_framework import serializers

from .models import SendOTPModel
class SendOTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendOTPModel
        fields = "__all__"