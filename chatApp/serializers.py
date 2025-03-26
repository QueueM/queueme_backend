from rest_framework import serializers

from .models import ChatRoomModel, ChatHistoryModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
class ChatRoomSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ChatRoomModel
        fields = "__all__"

class ChatHistorySerializer(CustomBaseModelSerializer):
    class Meta:
        model = ChatHistoryModel
        fields = "__all__"