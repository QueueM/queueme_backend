
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomersDetailsModelViewSet

router = DefaultRouter()
router.register(r'customers', CustomersDetailsModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('register/', RegisterAsCompanyAPIView.as_view())
    
]
