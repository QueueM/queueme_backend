from rest_framework import serializers
from .models import NotificationModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class NotificationsSerializer(CustomBaseModelSerializer):
    class Meta:
        model = NotificationModel
        fields = "__all__"
