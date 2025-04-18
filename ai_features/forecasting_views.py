# File: ai_features/forecasting_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    ForecastingRequestSerializer,
    ForecastingResponseSerializer,
)

@extend_schema(
    request=ForecastingRequestSerializer,
    responses=ForecastingResponseSerializer,
)
class ForecastingAPIView(GenericAPIView):
    serializer_class = ForecastingRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forecast = generate_forecast(serializer.validated_data)
        return Response({'forecast': forecast})
