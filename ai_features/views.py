from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .recommendations import train_recommendation_model, get_recommendations_for_user, get_marketing_offers

class PersonalizedMarketingAPIView(APIView):
    """
    GET: Returns personalized recommendations and marketing offers.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        try:
            algo = train_recommendation_model()
            recommendations = get_recommendations_for_user(user_id, algo, top_n=5)
            offers = get_marketing_offers(user_id, recommendations)
            return Response({
                "recommendations": [{"service_id": s, "predicted_rating": r} for s, r in recommendations],
                "marketing_offers": offers
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
