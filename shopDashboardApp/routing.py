# shopDashboardApp/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # URL for shop-specific dashboard updates
    re_path(r"ws/dashboard/shop/(?P<shop_id>\d+)/$", consumers.QueueDashboardConsumer.as_asgi()),
    # URL for company-specific dashboard updates
    re_path(r"ws/dashboard/company/(?P<company_id>\d+)/$", consumers.QueueDashboardConsumer.as_asgi()),
]
