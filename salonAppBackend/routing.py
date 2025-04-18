from chatApp.routing import websocket_urlpatterns as chat_patterns
from shopDashboardApp.routing import websocket_urlpatterns as dashboard_patterns
from reelsApp.routing import websocket_urlpatterns as reels_patterns
from storiesApp.routing import websocket_urlpatterns as stories_patterns

websocket_urlpatterns = chat_patterns + dashboard_patterns + reels_patterns + stories_patterns
