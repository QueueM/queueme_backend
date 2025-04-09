# chatApp/serializers.py
from rest_framework import serializers
from .models import ChatRoomModel, ChatHistoryModel
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class ChatRoomSerializer(CustomBaseModelSerializer):
    class Meta:
        model = ChatRoomModel
        fields = "__all__"

class ChatHistorySerializer(CustomBaseModelSerializer):
    # Adding an extra AI field, e.g., for the bot's response.
    # (Note: since the bot messages are stored as separate records,
    # this field may be used to optionally display a computed bot response.)
    bot_response = serializers.CharField(read_only=True, allow_blank=True)

    class Meta:
        model = ChatHistoryModel
        fields = "__all__"
