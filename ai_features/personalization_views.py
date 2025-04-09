from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .personalization import segment_users

class PersonalizationAPIView(APIView):
    """
    GET: Returns user segments based on booking behavior.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            segments = segment_users(n_clusters=3)
            return Response({"segments": segments})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
