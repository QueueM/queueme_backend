from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UpdateProfileSuggest, RegisterUserAPIView, UserProfileViewSet
router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path("register/", RegisterUserAPIView.as_view())
    
    ]
