# File: ai_features/sentiment_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    SentimentRequestSerializer,
    SentimentResponseSerializer,
)
from ai_features.sentiment import analyze_sentiment

@extend_schema(
    request=SentimentRequestSerializer,
    responses=SentimentResponseSerializer,
)
class SentimentAnalysisAPIView(GenericAPIView):
    serializer_class = SentimentRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        sentiment, score = analyze_sentiment(data.validated_data['text'])
        return Response({'sentiment': sentiment, 'score': score})

urlpatterns = [
    path('', SentimentAnalysisAPIView.as_view(), name='sentiment-analysis'),
]
