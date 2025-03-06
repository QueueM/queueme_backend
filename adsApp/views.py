from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import ShopAdsModel, ShopAdsImpressionModel
from .serializers import ShopAdsSerializer, ShopAdsImpressionSerializer
from .filters import ShopAdsFilter, ShopAdsImpressionFilter

class ShopAdViewSet(CustomBaseModelViewSet):
    queryset = ShopAdsModel.objects.all()
    serializer_class = ShopAdsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopAdsFilter

    @action(detail=False, methods=["get"])
    def fetch_ad(self, request):
        """ Fetch an ad and deduct credits from the advertiser """
        ad = ShopAdsModel.objects.order_by("?").first()  # Random ad
        if not ad:
            return Response({"message": "No ads available"}, status=status.HTTP_404_NOT_FOUND)

        advertiser = ad.shop
        cost_per_fetch = 1

        with transaction.atomic():
            if not ad.deduct_budget(1):
                return Response({"error": "Insufficient balance"}, status=status.HTTP_403_FORBIDDEN)
        serilaizer = ShopAdsSerializer(ad)
        return Response(serilaizer.data, status=status.HTTP_200_OK)
    
class ShopAdImpressionViewset(CustomBaseModelViewSet):
    queryset = ShopAdsImpressionModel.objects.all()
    serializer_class = ShopAdsImpressionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopAdsImpressionFilter