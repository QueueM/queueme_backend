# shopApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopDetailsViewSet,
    ShopGalleryImagesModelViewSet,
    ShopSpecialistDetailsModelViewSet,
    SpecialistTypesModelViewSet,
    DashboardLogViewSet,
)

app_name = "shopApp"

router = DefaultRouter()
router.register(r'shops', ShopDetailsViewSet, basename='shops')
router.register(r'gallery', ShopGalleryImagesModelViewSet, basename='gallery')
router.register(r'specialists', ShopSpecialistDetailsModelViewSet, basename='specialists')
router.register(r'specialists-types', SpecialistTypesModelViewSet, basename='specialists-types')
router.register(r'dashboard', DashboardLogViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('service/', include('shopServiceApp.urls')),  # If you have additional service-related URLs.
]
