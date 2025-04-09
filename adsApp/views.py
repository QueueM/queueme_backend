from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F, Q, Count
# Create your views here.
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import ShopAdsModel, ShopAdsImpressionModel
from .serializers import ShopAdsSerializer, ShopAdsImpressionSerializer
from .filters import ShopAdsFilter, ShopAdsImpressionFilter
from geopy.distance import geodesic
import random
class ShopAdViewSet(CustomBaseModelViewSet):
    queryset = ShopAdsModel.objects.all()
    serializer_class = ShopAdsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopAdsFilter

    @action(detail=False, methods=["get"])
    def fetch_adold(self, request):
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
    
    @action(detail=False, methods=["get"])
    def fetch_ad(self, request):
        user = request.user
        user_lat = request.query_params.get("latitude")
        user_long = request.query_params.get("longitude")
        user_gender = user.customer.gender  # Assuming gender is stored in `profile`

        if not user_lat or not user_long:
            return Response({"message":"Location is required"} ,status=status.HTTP_400_BAD_REQUEST)
        
        user_location = (float(user_lat), float(user_long))

        ads = ShopAdsModel.objects.filter(
            is_active=True,
            end_date__gte=now(),
        )

        ads = ads.filter(Q(target_gender=user_gender) | Q(target_gender="both"))

        ads = ads.annotate(click_count=Count("shopadsimpressionmodel"))

        ads = sorted(ads, key=lambda ad: (
            geodesic(user_location, (ad.latitude, ad.longitude)).km if ad.latitude and ad.longitude else float("inf"),
            -ad.budget, # Higher budget first
            -ad.click_count,  # More engagement first
            ad.start_date # Newer ads first
        ))

        random.shuffle(ads[:5])
        ad = ads[0] if ads else None

        if not ad:
            return Response({"message": "No ads available"}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            ad.deduct_budget(1)
        
        serializer = ShopAdsSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ShopAdImpressionViewset(CustomBaseModelViewSet):
    queryset = ShopAdsImpressionModel.objects.all()
    serializer_class = ShopAdsImpressionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ShopAdsImpressionFilter