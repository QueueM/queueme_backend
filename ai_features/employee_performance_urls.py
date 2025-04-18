# File: ai_features/employee_performance_urls.py
from django.urls import path
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from ai_features.serializers import (
    EmployeePerformanceRequestSerializer,
    EmployeePerformanceResponseSerializer,
)
from ai_features.employee_performance import calculate_performance

@extend_schema(
    request=EmployeePerformanceRequestSerializer,
    responses=EmployeePerformanceResponseSerializer,
)
class EmployeePerformanceAPIView(GenericAPIView):
    serializer_class = EmployeePerformanceRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)
        score, metrics = calculate_performance(data.validated_data)
        return Response({'performance_score': score, 'metrics': metrics})

urlpatterns = [
    path('', EmployeePerformanceAPIView.as_view(), name='employee-performance'),
]
