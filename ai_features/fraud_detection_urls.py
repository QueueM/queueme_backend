from django.urls import path
from .fraud_detection_views import FraudDetectionAPIView

urlpatterns = [
    path('', FraudDetectionAPIView.as_view(), name='fraud_detection'),
]
