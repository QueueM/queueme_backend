from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework import viewsets
from .models import ShopDetailsModel, ShopPermissionsModel, ShopGalleryImagesModel, ShopSpecialistDetailsModel
from .serializers import ShopDetailsModelSerializer, ShopPermissionsModelSerializer, ShopGalleryImagesModelSerializer, ShopSpecialistDetailsModelSerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .filters import ShopGalleryImagesFilter
class ShopDetailsViewSet(viewsets.ModelViewSet):
    queryset = ShopDetailsModel.objects.all()
    serializer_class = ShopDetailsModelSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Pass the user into the context
        return context


class ShopPermissionsViewSet(viewsets.ModelViewSet):
    queryset = ShopPermissionsModel.objects.all()
    serializer_class = ShopPermissionsModelSerializer

class ShopGalleryImagesModelViewSet(viewsets.ModelViewSet):
    queryset = ShopGalleryImagesModel.objects.all()
    serializer_class = ShopGalleryImagesModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopGalleryImagesFilter

class ShopSpecialistDetailsModelViewSet(CustomBaseModelViewSet):
    queryset = ShopSpecialistDetailsModel.objects.all()
    serializer_class = ShopSpecialistDetailsModelSerializer