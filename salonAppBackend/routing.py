# salonAppBackend/routing.py

from chatApp.routing import websocket_urlpatterns as chat_patterns
from shopDashboardApp.routing import websocket_urlpatterns as dashboard_patterns

websocket_urlpatterns = chat_patterns + dashboard_patterns
