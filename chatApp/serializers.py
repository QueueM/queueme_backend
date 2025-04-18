from rest_framework import serializers
from .models import ChatRoomModel, ChatHistoryModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class ChatRoomSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ChatRoomModel
        fields = "__all__"

class ChatHistorySerializer(CustomBaseModelSerializer):
    bot_response = serializers.CharField(read_only=True, allow_blank=True)
    class Meta:
        model = ChatHistoryModel
        fields = "__all__"
