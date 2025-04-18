# File: payment/urls.py

from django.urls import path
from .views import PaymentCreateAPIView, PaymentProcessingAPIView, DemoPaymentAPIView

urlpatterns = [
    path('create/', PaymentCreateAPIView.as_view(), name="payment-create"),
    path('process/', PaymentProcessingAPIView.as_view(), name="payment-process"),
    path('demo/', DemoPaymentAPIView.as_view(), name="demo-payment"),
]
