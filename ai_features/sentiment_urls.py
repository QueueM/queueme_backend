from django.urls import path
from .sentiment_views import SentimentAnalysisAPIView

urlpatterns = [
    path('', SentimentAnalysisAPIView.as_view(), name='sentiment_analysis'),
]
