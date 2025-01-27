



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterAsCompanyAPIView, CompanyDetailsViewSet, CompanyEmployeeDetailsModelViewSet

router = DefaultRouter()
router.register(r'companies', CompanyDetailsViewSet)
router.register(r'employees', CompanyEmployeeDetailsModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAsCompanyAPIView.as_view())
    
]
