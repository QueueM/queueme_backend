from django.urls import path
from .personalization_views import PersonalizationAPIView

urlpatterns = [
    path('', PersonalizationAPIView.as_view(), name='personalization'),
]
