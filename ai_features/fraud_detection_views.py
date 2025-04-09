from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .fraud_detection import detect_fraud

class FraudDetectionAPIView(APIView):
    """
    GET: Returns bookings flagged as anomalous.
    """
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        try:
            anomalies = detect_fraud()
            return Response({"anomalies": anomalies})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
