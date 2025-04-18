# File: shopApp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopDetailsViewSet,
    ShopGalleryImagesModelViewSet,
    ShopSpecialistDetailsModelViewSet,
    SpecialistTypesModelViewSet,
)

app_name = "shopApp"
router = DefaultRouter()
router.register(r'shops', ShopDetailsViewSet, basename='shops')
router.register(r'gallery', ShopGalleryImagesModelViewSet, basename='gallery')
router.register(r'specialists', ShopSpecialistDetailsModelViewSet, basename='specialists')
router.register(r'specialists-types', SpecialistTypesModelViewSet, basename='specialists-types')

urlpatterns = [
    path('', include(router.urls)),
    path('service/', include('shopServiceApp.urls')),
]
