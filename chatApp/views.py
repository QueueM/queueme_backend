from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import ChatHistorySerializer, ChatRoomSerializer
from .filters import ChatHistoryFilter, ChatRoomFilter
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import ChatRoomModel, ChatHistoryModel

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