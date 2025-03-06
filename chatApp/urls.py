

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ChatRoomModelViewSet, ChatHistorySerializerModelViewSet
router = DefaultRouter()


router.register(r'room', ChatRoomModelViewSet)
router.register(r'history', ChatHistorySerializerModelViewSet)

urlpatterns = [
     path('', include(router.urls))
]