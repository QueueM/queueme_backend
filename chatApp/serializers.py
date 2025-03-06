from rest_framework import serializers

from .models import ChatRoomModel, ChatHistoryModel

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoomModel
        fields = "__all__"

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistoryModel
        fields = "__all__"