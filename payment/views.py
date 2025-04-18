# File: payment/views.py
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema

from .serializers import (
    PaymentCreateRequestSerializer,
    PaymentCreateResponseSerializer,
    PaymentProcessingRequestSerializer,
    PaymentProcessingResponseSerializer,
    DemoPaymentResponseSerializer,
)
from .services import initiate_payment, process_payment_callback

logger = logging.getLogger(__name__)

@extend_schema(
    request=PaymentCreateRequestSerializer,
    responses=PaymentCreateResponseSerializer,
)
class PaymentCreateAPIView(GenericAPIView):
    """
    Initiates a payment.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentCreateRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result, payment_record = initiate_payment(
                data['payment_for'],
                data['amount'],
                data.get('source', {}),
                data.get('metadata', {}),
                data.get('description', '')
            )
            return Response(
                {'payment': result, 'payment_record_id': payment_record.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception("Payment initiation error: %s", e)
            return Response(
                {'error': 'Payment initiation failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    request=PaymentProcessingRequestSerializer,
    responses=PaymentProcessingResponseSerializer,
)
class PaymentProcessingAPIView(GenericAPIView):
    """
    Verifies payment callback processing.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentProcessingRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result = process_payment_callback(
                data['payment_id'],
                wallet_type=data['payment_for']
            )
            status_str = result.get('status', 'Unknown')
            logger.info("Payment callback processed: %s", status_str)
            return Response({'payment_status': status_str}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Payment processing error: %s", e)
            return Response(
                {'error': 'Payment processing failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    responses=DemoPaymentResponseSerializer,
)
class DemoPaymentAPIView(GenericAPIView):
    """
    Demo endpoint for payment creation.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        payment_for = request.query_params.get('payment_for', 'subscription')
        amount = request.query_params.get('amount', 100)
        source = {
            'name': 'Demo User',
            'number': '4111111111111111',
            'cvc': '123',
            'month': 12, 'year': 2029,
            '3ds': True, 'manual': False, 'save_card': False
        }
        metadata = {
            'subscription_id': request.query_params.get('subscription_id', ''),
            'user_id': request.query_params.get('user_id', 1),
            'bill_name': 'Demo Bill',
            'billing_cycle': request.query_params.get('billing_cycle', 'monthly'),
            'payment_type': 'p'
        }
        try:
            result, payment_record = initiate_payment(
                payment_for, amount, source, metadata, 'Demo Payment'
            )
            return Response(
                {'demo_payment': result, 'payment_record_id': payment_record.id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception("Demo payment error: %s", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

