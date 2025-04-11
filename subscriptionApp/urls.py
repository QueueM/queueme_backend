"""
subscriptionApp/urls.py

Routes for the subscription app.
Includes routes for subscription plan management, payments, and demo payment endpoint.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanySubscriptionPlanViewSet,
    PaymentCreateApiView,
    PaymentProcessingAPIView,
    DemoPaymentApiView,
    CompanySubscriptionPlanDetailsAPIView
)

router = DefaultRouter()
router.register(r'company-plans', CompanySubscriptionPlanViewSet, basename='company-plans')

urlpatterns = [
    path('', include(router.urls)),
    path("payment/", PaymentCreateApiView.as_view(), name="payment"),
    path("payment/process/", PaymentProcessingAPIView.as_view(), name="payment-check"),
    path("demo/payment/", DemoPaymentApiView.as_view(), name="demo-payment"),
    path("company-plan-details/", CompanySubscriptionPlanDetailsAPIView.as_view(), name="subscription_details"),
]
