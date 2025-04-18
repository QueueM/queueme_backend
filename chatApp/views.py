# File: chatApp/views.py

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .serializers import ChatRoomSerializer, ChatHistorySerializer
from .filters import ChatRoomFilter, ChatHistoryFilter
from .models import ChatRoomModel, ChatHistoryModel

class ChatRoomModelViewSet(CustomBaseModelViewSet):
    """
    ViewSet for listing and managing chat rooms.
    """
    queryset = ChatRoomModel.objects.all()
    serializer_class = ChatRoomSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ChatRoomFilter

class ChatHistoryModelViewSet(CustomBaseModelViewSet):
    """
    ViewSet for listing and managing chat history entries.
    """
    queryset = ChatHistoryModel.objects.all()
    serializer_class = ChatHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ChatHistoryFilter

    def perform_create(self, serializer):
        """
        Hook into creation of a chat message. Customize as needed.
        """
        instance = serializer.save()
        # Optionally add post-save logic here, e.g.:
        # sentiment = analyze_sentiment(instance.message)
        # recommendations = get_ai_recommendations(instance)
        # send notifications, etc.
        return instance

