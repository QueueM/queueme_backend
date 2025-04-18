# File: ai_features/fraud_detection_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    FraudDetectionRequestSerializer,
    FraudDetectionResponseSerializer,
)

@extend_schema(
    request=FraudDetectionRequestSerializer,
    responses=FraudDetectionResponseSerializer,
)
class FraudDetectionAPIView(GenericAPIView):
    serializer_class = FraudDetectionRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_fraud, probability = detect_fraud(serializer.validated_data)
        return Response({'is_fraud': is_fraud, 'probability': probability})

