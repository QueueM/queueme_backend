# shopServiceApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopServiceCategoryViewSet,
    ShopServiceDetailsViewSet,
    ServiceExtendedDetailsViewSet,
    ServiceBookingDetailsViewSet,
    ServiceBookingDiscountCouponsViewSet,
    ShopServiceGalleryModelViewSet,
)

app_name = "shopServiceApp"

router = DefaultRouter()
router.register(r'categories', ShopServiceCategoryViewSet, basename='categories')
router.register(r'services', ShopServiceDetailsViewSet, basename='services')
router.register(r'service-extended-details', ServiceExtendedDetailsViewSet, basename='service-extended-details')
router.register(r'services-bookings', ServiceBookingDetailsViewSet, basename='services-bookings')
router.register(r'coupons', ServiceBookingDiscountCouponsViewSet, basename='coupons')
router.register(r'gallery', ShopServiceGalleryModelViewSet, basename='gallery')

urlpatterns = [
    path('', include(router.urls)),
]
