from django.urls import re_path
from .consumers import ReelsConsumer

websocket_urlpatterns = [
    re_path(r'ws/reels/(?P<reel_id>\d+)/$', ReelsConsumer.as_asgi()),
]
