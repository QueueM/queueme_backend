from django.urls import path
from .consumers import StoriesConsumer

websocket_urlpatterns = [
    path('ws/stories/<int:story_id>/', StoriesConsumer.as_asgi()),
]
