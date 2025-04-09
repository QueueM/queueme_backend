from rest_framework import viewsets
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceGalleryModel
)
from .serializers import (
    ShopServiceCategoryModelSerializer,
    ShopServiceDetailsModelSerializer,
    ServiceBookingDetailsModelSerializer,
    ServiceBookingDiscountCouponsModelSerializer,
    ShopServiceGalleryModelSerializer
)
from .filters import (
    ShopServiceCategoryFilter,
    ShopServiceDetailsFilter,
    ServiceBookingDetailsFilter,
    ShopServiceGalleryFilter
)

class ShopServiceCategoryViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceCategoryModel.objects.all()
    serializer_class = ShopServiceCategoryModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', 'created_at']
    filterset_class = ShopServiceCategoryFilter

class ShopServiceDetailsViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceDetailsModel.objects.all()
    serializer_class = ShopServiceDetailsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'duration', 'created_at']
    filterset_class = ShopServiceDetailsFilter

class ServiceBookingDetailsViewSet(CustomBaseModelViewSet):
    queryset = ServiceBookingDetailsModel.objects.all()
    serializer_class = ServiceBookingDetailsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['booking_date', 'booking_time', 'created_at', 'status']
    filterset_class = ServiceBookingDetailsFilter

class ServiceBookingDiscountCouponsViewSet(CustomBaseModelViewSet):
    queryset = ServiceBookingDiscountCouponsModel.objects.all()
    serializer_class = ServiceBookingDiscountCouponsModelSerializer

class ShopServiceGalleryModelViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceGalleryModel.objects.all()
    serializer_class = ShopServiceGalleryModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id']
    filterset_class = ShopServiceGalleryFilter
