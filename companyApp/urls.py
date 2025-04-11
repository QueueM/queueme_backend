# companyApp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAsCompanyAPIView, CompanyDetailsViewSet

app_name = "companyApp"  # Add the app name here

router = DefaultRouter()
router.register(r'companies', CompanyDetailsViewSet, basename='companies')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAsCompanyAPIView.as_view(), name='company-register'),
]
