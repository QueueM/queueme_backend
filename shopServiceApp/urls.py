from django.urls import path, include
from .views import ShopServiceDetailsViewSet, ShopServiceCategoryViewSet, ServiceBookingDetailsViewSet, ServiceBookingDiscountCouponsViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'services', ShopServiceDetailsViewSet)
router.register(r'services-categories', ShopServiceCategoryViewSet)
router.register(r'services-bookings', ServiceBookingDetailsViewSet)
router.register(r'services-bookingdiscounts', ServiceBookingDiscountCouponsViewSet)

urlpatterns = [
     path('', include(router.urls)),
    ]
