

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CompanySubscriptionPlanViewSet
router = DefaultRouter()
router.register(r'company-plans', CompanySubscriptionPlanViewSet)

urlpatterns = [
     path('', include(router.urls)),
    ]