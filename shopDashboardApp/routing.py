# shopDashboardApp/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/dashboard/shop/(?P<shop_id>\d+)/$",
        consumers.QueueDashboardConsumer.as_asgi()
    ),
    re_path(
        r"ws/dashboard/company/(?P<company_id>\d+)/$",
        consumers.QueueDashboardConsumer.as_asgi()
    ),
]
