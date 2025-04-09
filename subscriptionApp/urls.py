

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CompanySubscriptionPlanViewSet , PaymentCreateApiView  , PaymentProcessingAPIView , DemoPaymentApiView, CompanySubscriptionPlanDetailsAPIView )
router = DefaultRouter()
router.register(r'company-plans', CompanySubscriptionPlanViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path("payment/", PaymentCreateApiView.as_view(), name="payment"),
     path("payment/process/",PaymentProcessingAPIView.as_view(), name="payment-check"),
     path("demo/payment/" , DemoPaymentApiView.as_view() , name="demo-payment"),
     path("company-plan-details/" , CompanySubscriptionPlanDetailsAPIView.as_view() , name="subscription_details"),
    ]
