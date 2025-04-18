from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopAdViewSet, ShopAdImpressionViewset

router = DefaultRouter()
router.register(r'shop-ads', ShopAdViewSet)
router.register(r'shop-ads-impression', ShopAdImpressionViewset)

urlpatterns = [
    path('', include(router.urls)),
]
