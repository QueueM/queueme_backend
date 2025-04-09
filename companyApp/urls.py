from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAsCompanyAPIView, CompanyDetailsViewSet

router = DefaultRouter()
router.register(r'companies', CompanyDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAsCompanyAPIView.as_view(), name='company-register'),
]
