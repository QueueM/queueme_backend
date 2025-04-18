from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer
from ai_features import sentiment
import logging

logger = logging.getLogger(__name__)

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        if review.comment:
            try:
                score = sentiment.analyze(review.comment)
                review.sentiment_score = score
                review.save(update_fields=['sentiment_score'])
            except Exception as e:
                logger.error(f"Error analyzing sentiment for review {review.id}: {e}")
