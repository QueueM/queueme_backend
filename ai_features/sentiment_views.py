from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .sentiment import analyze_sentiment

class SentimentAnalysisAPIView(APIView):
    """
    POST: Accepts review text and returns its sentiment.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        review_text = request.data.get("review_text", "")
        if not review_text:
            return Response({"error": "No review_text provided."}, status=400)
        sentiment = analyze_sentiment(review_text)
        return Response(sentiment)
