# salonAppBackend/routing.py

from chatApp.routing import websocket_urlpatterns as chat_patterns
from shopDashboardApp.routing import websocket_urlpatterns as dashboard_patterns

# Combine all WebSocket URL patterns from different apps
websocket_urlpatterns = chat_patterns + dashboard_patterns
