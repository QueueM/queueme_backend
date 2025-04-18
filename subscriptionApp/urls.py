# File: subscriptionApp/urls.py

from django.urls import path
from .views import (
    CompanySubscriptionPlanDetailsAPIView,
    SubscriptionPaymentIntegrationAPIView,
)

urlpatterns = [
    path('plans/<int:plan_id>/', CompanySubscriptionPlanDetailsAPIView.as_view(), name='subscription-plan-details'),
    path('integrate-payment/', SubscriptionPaymentIntegrationAPIView.as_view(), name='subscription-payment-integration'),
]
