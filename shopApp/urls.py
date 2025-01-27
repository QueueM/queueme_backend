from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShopDetailsViewSet, ShopGalleryImagesModelViewSet, ShopSpecialistDetailsModelViewSet
router = DefaultRouter()
router.register(r'shops', ShopDetailsViewSet)
router.register(r'gallery', ShopGalleryImagesModelViewSet)
router.register(r'specialists', ShopSpecialistDetailsModelViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('service/', include('shopServiceApp.urls'))
    ]
