# File: chatApp/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ChatRoomModelViewSet, ChatHistoryModelViewSet

router = DefaultRouter()
router.register(r'rooms', ChatRoomModelViewSet, basename='chatroom')
router.register(r'history', ChatHistoryModelViewSet, basename='chathistory')

urlpatterns = [
    path('', include(router.urls)),
]