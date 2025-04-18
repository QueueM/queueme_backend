# File: ai_features/sentiment_views.py
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializers import (
    SentimentRequestSerializer,
    SentimentResponseSerializer,
)

@extend_schema(
    request=SentimentRequestSerializer,
    responses=SentimentResponseSerializer,
)
class SentimentAnalysisAPIView(GenericAPIView):
    serializer_class = SentimentRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sentiment, score = analyze_sentiment(serializer.validated_data['text'])
        return Response({'sentiment': sentiment, 'score': score})

