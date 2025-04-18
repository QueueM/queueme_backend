# File: ai_features/forecasting_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    ForecastingRequestSerializer,
    ForecastingResponseSerializer,
)
from ai_features.forecasting import generate_forecast

@extend_schema(
    request=ForecastingRequestSerializer,
    responses=ForecastingResponseSerializer,
)
class ForecastingAPIView(GenericAPIView):
    serializer_class = ForecastingRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        forecast = generate_forecast(data.validated_data)
        return Response({'forecast': forecast})

urlpatterns = [
    path('', ForecastingAPIView.as_view(), name='forecasting'),
]
