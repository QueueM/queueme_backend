# chatApp/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .serializers import ChatRoomSerializer, ChatHistorySerializer
from .filters import ChatRoomFilter, ChatHistoryFilter
from .models import ChatRoomModel, ChatHistoryModel

# Import the chatbot AI module and additional AI utilities.
from ai_features import chatbot
from customClasses.ai_utils import analyze_sentiment, get_ai_recommendations

class ChatRoomModelViewSet(CustomBaseModelViewSet):
    queryset = ChatRoomModel.objects.all()
    serializer_class = ChatRoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ChatRoomFilter

class ChatHistorySerializerModelViewSet(CustomBaseModelViewSet):
    queryset = ChatHistoryModel.objects.all()
    serializer_class = ChatHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ChatHistoryFilter

    def perform_create(self, serializer):
        # Save the incoming chat message.
        instance = serializer.save()
        # If the message is sent by a user (sent_by == 1), then generate a bot response.
        if instance.sent_by == 1:
            # Optionally, analyze the sentiment of the user's message.
            sentiment = analyze_sentiment(instance.message)
            # Optionally, get extra recommendations based on the user's message.
            recommendations = get_ai_recommendations(instance)
            # (Optional) Log or use sentiment and recommendations values.
            # For demonstration, these values might be logged or stored separately.
            # Generate the bot response using the chatbot module.
            bot_reply = chatbot.get_response(instance.message, self.request.user)
            # Create a new ChatHistoryModel instance for the bot's reply.
            ChatHistoryModel.objects.create(
                room=instance.room,
                sent_by=3,  # Use a designated code for the bot sender (e.g., 3).
                message=bot_reply
            )
