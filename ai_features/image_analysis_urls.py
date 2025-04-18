# File: ai_features/image_analysis_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    ImageAnalysisRequestSerializer,
    ImageAnalysisResponseSerializer,
)
from ai_features.image_analysis import analyze_image

@extend_schema(
    request=ImageAnalysisRequestSerializer,
    responses=ImageAnalysisResponseSerializer,
)
class ImageAnalysisAPIView(GenericAPIView):
    serializer_class = ImageAnalysisRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        analysis = analyze_image(data.validated_data['image_url'])
        return Response({'analysis': analysis})

urlpatterns = [
    path('', ImageAnalysisAPIView.as_view(), name='image-analysis'),
]
