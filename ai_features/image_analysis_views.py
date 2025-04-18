# File: ai_features/image_analysis_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    ImageAnalysisRequestSerializer,
    ImageAnalysisResponseSerializer,
)

@extend_schema(
    request=ImageAnalysisRequestSerializer,
    responses=ImageAnalysisResponseSerializer,
)
class ImageAnalysisAPIView(GenericAPIView):
    serializer_class = ImageAnalysisRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        analysis = analyze_image(serializer.validated_data['image_url'])
        return Response({'analysis': analysis})

