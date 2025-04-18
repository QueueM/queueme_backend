# File: ai_features/churn_prediction_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    ChurnPredictionRequestSerializer,
    ChurnPredictionResponseSerializer,
)
from ai_features.churn_prediction import calculate_churn_risk

@extend_schema(
    request=ChurnPredictionRequestSerializer,
    responses=ChurnPredictionResponseSerializer,
)
class ChurnPredictionAPIView(GenericAPIView):
    serializer_class = ChurnPredictionRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        customer_id = data.validated_data['customer_id']
        history = data.validated_data['history']
        result = calculate_churn_risk(customer_id, history)
        return Response(result)

urlpatterns = [
    path('', ChurnPredictionAPIView.as_view(), name='churn-predict'),
]
