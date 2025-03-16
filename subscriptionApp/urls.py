

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CompanySubscriptionPlanViewSet , PaymentApiView)
router = DefaultRouter()
router.register(r'company-plans', CompanySubscriptionPlanViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path("payment/", PaymentApiView.as_view(), name="payment")
    ]