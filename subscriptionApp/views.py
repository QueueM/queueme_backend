# File: subscriptionApp/views.py

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel
from .serializers import (
    CompanySubscriptionPlanSerializer,
    CompanySubscriptionDetailsSerializer,
    SubscriptionPaymentIntegrationRequestSerializer,
    SubscriptionPaymentIntegrationResponseSerializer,
)

@extend_schema(
    responses=CompanySubscriptionPlanSerializer,
)
class CompanySubscriptionPlanDetailsAPIView(GenericAPIView):
    """
    GET /subscription/plans/{plan_id}/
    Retrieves detailed info about a specific subscription plan.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CompanySubscriptionPlanSerializer

    def get(self, request, plan_id, *args, **kwargs):
        try:
            plan = CompanySubscriptionPlansModel.objects.get(pk=plan_id)
        except CompanySubscriptionPlansModel.DoesNotExist:
            return Response({'detail': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=SubscriptionPaymentIntegrationRequestSerializer,
    responses=SubscriptionPaymentIntegrationResponseSerializer,
)
class SubscriptionPaymentIntegrationAPIView(GenericAPIView):
    """
    POST /subscription/integrate-payment/
    Integrates a completed payment with a company's subscription.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriptionPaymentIntegrationRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        subscription = CompanySubscriptionDetailsModel.objects.create(
            company_id=data['company'],
            plan_id=data['plan'],
            billing_cycle=data['billing_cycle'],
            # Optionally set start/end dates here
        )
        return Response({
            'message': 'Subscription payment integrated successfully.',
            'plan': data['plan'],
            'payment_id': data['payment_id'],
            'status': data['status'],
        }, status=status.HTTP_200_OK)

