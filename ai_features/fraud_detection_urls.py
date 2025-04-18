# File: ai_features/fraud_detection_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    FraudDetectionRequestSerializer,
    FraudDetectionResponseSerializer,
)
from ai_features.fraud_detection import detect_fraud

@extend_schema(
    request=FraudDetectionRequestSerializer,
    responses=FraudDetectionResponseSerializer,
)
class FraudDetectionAPIView(GenericAPIView):
    serializer_class = FraudDetectionRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        is_fraud, probability = detect_fraud(data.validated_data)
        return Response({'is_fraud': is_fraud, 'probability': probability})

urlpatterns = [
    path('', FraudDetectionAPIView.as_view(), name='fraud-detection'),
]
