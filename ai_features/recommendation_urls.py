# File: ai_features/recommendation_urls.py

from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import RecommendationResponseSerializer

# <-- FIXED import to match your file name: recommendations.py
from ai_features.recommendations import get_recommendations

@extend_schema(responses=RecommendationResponseSerializer)
class RecommendationAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        recs = get_recommendations()
        return Response({'recommendations': recs})

urlpatterns = [
    path('', RecommendationAPIView.as_view(), name='recommendations'),
]
