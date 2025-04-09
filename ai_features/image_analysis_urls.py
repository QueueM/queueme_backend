from django.urls import path
from .image_analysis_views import ImageAnalysisAPIView

urlpatterns = [
    path('', ImageAnalysisAPIView.as_view(), name='image_analysis'),
]
