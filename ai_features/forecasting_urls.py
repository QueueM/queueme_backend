from django.urls import path
from .forecasting_views import ForecastingAPIView

urlpatterns = [
    path('', ForecastingAPIView.as_view(), name='forecast'),
]
