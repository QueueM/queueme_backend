from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegistrationOTPAPIView, TestAPIView, RegisterAPIView, LoginWithOTPAPIView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-otp/', RegistrationOTPAPIView.as_view()),
    path('test/', TestAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('get-token-with-otp/', LoginWithOTPAPIView.as_view()),
]
