from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .recommendations import get_recommendations_for_user

class PersonalizedMarketingAPIView(APIView):
    """
    GET: Returns personalized recommendations and marketing offers for the user.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        recommendations = get_recommendations_for_user(user)
        return Response({"recommendations": recommendations}, status=200)
