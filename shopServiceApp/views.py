from django.shortcuts import render

# Create your views here.
from .models import ShopServiceDetailsModel, ShopServiceCategoryModel, ServiceBookingDiscountCouponsModel, ServiceBookingDetailsModel
from .serializers import ShopServiceCategoryModelSerializer, ShopServiceDetailsModelSerializer, ServiceBookingDetailsModelSerializer, ServiceBookingDiscountCouponsModelSerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import ShopServiceGalleryModel
from .serializers import ShopServiceGalleryModelSerializer
from .filters import ShopServiceGalleryFilter

class ShopServiceDetailsViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceDetailsModel.objects.all()
    serializer_class = ShopServiceDetailsModelSerializer

class ShopServiceCategoryViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceCategoryModel.objects.all()
    serializer_class = ShopServiceCategoryModelSerializer

class ServiceBookingDetailsViewSet(CustomBaseModelViewSet):
    queryset = ServiceBookingDetailsModel.objects.all()
    serializer_class = ServiceBookingDetailsModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Pass the user into the context
        return context
    
    # def perform_create(self, serializer):
    #     required_keys = ['service', 'booking_date']
        
    #     # Validate required keys
    #     missing_keys = [key for key in required_keys if key not in request.GET]
    #     if missing_keys:
    #         return Response(
    #             {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )
        
    #     service = serializer.validated_data['service']
    #     booking_date = serializer.validated_data['booking_date']
    #     booking_time = serializer.validated_data['booking_time']

    #     # Check for overlapping bookings
    #     overlapping_booking = ServiceBookingDetailsModel.objects.filter(
    #         service=service,
    #         booking_date=booking_date,
    #         booking_time=booking_time
    #     ).exists()

    #     if overlapping_booking:
    #         raise ValidationError("This time slot is already booked for the selected service.")

    #     serializer.save()

class ServiceBookingDiscountCouponsViewSet(CustomBaseModelViewSet):
    queryset = ServiceBookingDiscountCouponsModel.objects.all()
    serializer_class = ServiceBookingDiscountCouponsModelSerializer
    

class ShopGalleryImagesModelViewSet(CustomBaseModelViewSet):
    queryset = ShopServiceGalleryModel.objects.all()
    serializer_class = ShopServiceGalleryModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopServiceGalleryFilter