from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .forecasting import forecast_bookings

class ForecastingAPIView(APIView):
    """
    GET: Returns booking forecasts for the next N days.
    Query parameter: periods (default=30)
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        periods = int(request.query_params.get('periods', 30))
        try:
            forecast = forecast_bookings(periods=periods)
            return Response({"forecast": forecast})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
