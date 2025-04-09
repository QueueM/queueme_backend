from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopServiceCategoryViewSet,
    ShopServiceDetailsViewSet,
    ServiceBookingDetailsViewSet,
    ServiceBookingDiscountCouponsViewSet,
    ShopServiceGalleryModelViewSet
)

router = DefaultRouter()
router.register(r'categories', ShopServiceCategoryViewSet, basename='categories')
router.register(r'services', ShopServiceDetailsViewSet, basename='services')
# Change this registration: use "services-bookings" so that the URL becomes /shops/service/services-bookings/
router.register(r'services-bookings', ServiceBookingDetailsViewSet, basename='services-bookings')
router.register(r'coupons', ServiceBookingDiscountCouponsViewSet, basename='coupons')
router.register(r'gallery', ShopServiceGalleryModelViewSet, basename='gallery')

urlpatterns = [
    path('', include(router.urls)),
]
