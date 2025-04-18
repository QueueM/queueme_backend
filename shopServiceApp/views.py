# shopServiceApp/views.py

from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceExtendedDetailsModel,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceGalleryModel,
)
from .serializers import (
    ShopServiceCategoryModelSerializer,
    ShopServiceDetailsModelSerializer,
    ServiceExtendedDetailsModelSerializer,
    ServiceBookingDetailsModelSerializer,
    ServiceBookingDiscountCouponsModelSerializer,
    ShopServiceGalleryModelSerializer,
)
from .filters import (
    ShopServiceCategoryFilter,
    ShopServiceDetailsFilter,
    ServiceBookingDetailsFilter,
    ShopServiceGalleryFilter,
)
# Import DjangoFilterBackend to avoid the NameError.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

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

class ServiceExtendedDetailsViewSet(CustomBaseModelViewSet):
    queryset = ServiceExtendedDetailsModel.objects.all()
    serializer_class = ServiceExtendedDetailsModelSerializer

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
