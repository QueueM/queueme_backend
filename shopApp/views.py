# File: shopApp/views.py

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    SpecialistTypesModel,
)
from .serializers import (
    ShopDetailsModelSerializer,
    ShopGalleryImagesModelSerializer,
    ShopSpecialistDetailsModelSerializer,
    SpecialistTypesSerializer,
)

class IsCompanyOrOwnShop(BasePermission):
    """
    Custom permission: company users see only their branches;
    standalone shops see only their own.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(user, 'company'):
            return obj.company == user.company
        return obj.owner == user

class ShopDetailsViewSet(viewsets.ModelViewSet):
    """
    Manage shops. We provide a top‑level queryset and
    lookup_value_regex so Spectacular infers <pk> is int.
    """
    serializer_class   = ShopDetailsModelSerializer
    queryset           = ShopDetailsModel.objects.all()   # for schema introspection
    lookup_field       = 'pk'
    lookup_value_regex = r'\d+'                           # <int:pk>
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['shop_name', 'owner__username']
    ordering_fields    = ['created_at', 'shop_name']
    permission_classes = [IsAuthenticated, IsCompanyOrOwnShop]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company'):
            return ShopDetailsModel.objects.filter(company=user.company)
        return ShopDetailsModel.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        kwargs = {'owner': user}
        if hasattr(user, 'company'):
            kwargs['company'] = user.company
        serializer.save(**kwargs)

class ShopGalleryImagesModelViewSet(viewsets.ModelViewSet):
    queryset           = ShopGalleryImagesModel.objects.all()
    serializer_class   = ShopGalleryImagesModelSerializer
    permission_classes = [IsAuthenticated]

class ShopSpecialistDetailsModelViewSet(viewsets.ModelViewSet):
    queryset           = ShopSpecialistDetailsModel.objects.all()
    serializer_class   = ShopSpecialistDetailsModelSerializer
    permission_classes = [IsAuthenticated]

class SpecialistTypesModelViewSet(viewsets.ModelViewSet):
    queryset           = SpecialistTypesModel.objects.all()
    serializer_class   = SpecialistTypesSerializer
    permission_classes = [IsAuthenticated]
