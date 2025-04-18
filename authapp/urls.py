# File: authapp/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegistrationOTPAPIView,
    TestAPIView,
    RegisterAPIView,
    LoginWithOTPAPIView,
    UnifiedLoginWithOTPAPIView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-otp/', RegistrationOTPAPIView.as_view(), name='get_otp'),
    path('test/', TestAPIView.as_view(), name='test'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('get-token-with-otp/', LoginWithOTPAPIView.as_view(), name='login_with_otp'),
    path('unified-login/', UnifiedLoginWithOTPAPIView.as_view(), name='unified_login'),
]
