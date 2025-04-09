from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopDetailsViewSet,
    ShopGalleryImagesModelViewSet,
    ShopSpecialistDetailsModelViewSet,
    SpecialistTypesModelViewSet,
    DashboardLogViewSet
)

router = DefaultRouter()
router.register(r'shops', ShopDetailsViewSet, basename='shops')
router.register(r'gallery', ShopGalleryImagesModelViewSet, basename='gallery')
router.register(r'specialists', ShopSpecialistDetailsModelViewSet, basename='specialists')
router.register(r'specialists-types', SpecialistTypesModelViewSet, basename='specialists-types')
router.register(r'dashboard', DashboardLogViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    # This line includes the shopServiceApp URLs under "/shops/service/" 
    path('service/', include('shopServiceApp.urls')),
]
