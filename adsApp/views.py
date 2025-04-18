from django.db import transaction
from django.db.models import Count, Q
from django.utils.timezone import now
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import ShopAdsModel, ShopAdsImpressionModel
from .serializers import ShopAdsSerializer, ShopAdsImpressionSerializer
from .filters import ShopAdsFilter, ShopAdsImpressionFilter
import random, logging
from payment.services import initiate_payment

logger = logging.getLogger(__name__)

class ShopAdViewSet(CustomBaseModelViewSet):
    queryset = ShopAdsModel.objects.all()
    serializer_class = ShopAdsSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_class = ShopAdsFilter

    @action(detail=False, methods=["get"])
    def fetch_ad(self, request):
        user = request.user
        user_lat = request.query_params.get("latitude")
        user_long = request.query_params.get("longitude")
        user_gender = getattr(getattr(user, 'customer', None), 'gender', 'both')
        if not user_lat or not user_long:
            return Response({"message": "Location is required"}, status=status.HTTP_400_BAD_REQUEST)
        ads = ShopAdsModel.objects.filter(is_active=True, end_date__gte=now())
        ads = ads.filter(Q(target_gender=user_gender) | Q(target_gender="both"))
        ads = ads.annotate(click_count=Count("impressions"))
        ads = sorted(ads, key=lambda ad: (
            abs(ad.latitude - float(user_lat)) + abs(ad.longitude - float(user_long)) if ad.latitude and ad.longitude else float("inf"),
            -ad.budget,
            -ad.click_count,
            ad.start_date
        ))
        if not ads:
            return Response({"message": "No ads available"}, status=status.HTTP_404_NOT_FOUND)
        ad = ads[0]
        with transaction.atomic():
            if not ad.deduct_budget(1):
                return Response({"error": "Insufficient ad budget"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ShopAdsSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def purchase_ad_credit(self, request):
        amount = request.data.get("amount")
        source = request.data.get("source", {})
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        metadata = {
            "user_id": request.user.id,
            "bill_name": request.user.username,
            "payment_type": "p",
            "ads_purchase": True
        }
        try:
            result, payment_record = initiate_payment("ads", amount, source, metadata, "Ads Credit Purchase")
            shop = request.user.customer.shop
            shop.credits += int(float(amount))
            shop.save()
            return Response({
                "payment": result,
                "payment_record_id": payment_record.id,
                "new_credits": shop.credits
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error purchasing ad credits: %s", e)
            return Response({"error": "Ad credit purchase failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ShopAdImpressionViewset(CustomBaseModelViewSet):
    queryset = ShopAdsImpressionModel.objects.all()
    serializer_class = ShopAdsImpressionSerializer
    filter_backends = [filters.OrderingFilter]
    filterset_class = ShopAdsImpressionFilter
