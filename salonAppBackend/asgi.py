import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salonAppBackend.settings')

django.setup()  # Ensure Django is initialized before importing models

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chatApp.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
