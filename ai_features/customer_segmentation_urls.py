# File: ai_features/customer_segmentation_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    CustomerSegmentationRequestSerializer,
    CustomerSegmentationResponseSerializer,
)
from ai_features.customer_segmentation import segment_customers

@extend_schema(
    request=CustomerSegmentationRequestSerializer,
    responses=CustomerSegmentationResponseSerializer,
)
class CustomerSegmentationAPIView(GenericAPIView):
    serializer_class = CustomerSegmentationRequestSerializer

    def post(self, request, *args, **kwargs):
        shop_id = self.get_serializer(data=request.data).validated_data['shop_id']
        segments = segment_customers(shop_id)
        return Response({'segments': segments})

urlpatterns = [
    path('', CustomerSegmentationAPIView.as_view(), name='customer-segmentation'),
]
