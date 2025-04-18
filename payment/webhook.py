# File: payment/webhook.py
import logging
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import WebhookRequestSerializer, WebhookResponseSerializer
from .models import Payment

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class WebHookApiView(GenericAPIView):
    """
    Processes payment gateway webhooks.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = WebhookRequestSerializer

    @extend_schema(
        request=WebhookRequestSerializer,
        responses=WebhookResponseSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['data']
        metadata = data['metadata']
        payment_id = data['id']
        status_payment = data['status']
        try:
            payment_obj, created = Payment.objects.get_or_create(
                payment_id=payment_id,
                defaults={
                    'amount': data['amount'],
                    'status': status_payment,
                    'payment_type': metadata.get('payment_type', 'p'),
                    'payment_for': metadata['payment_for'],
                    'bill_name': metadata.get('bill_name', ''),
                    'phone_number': metadata.get('phone_number', ''),
                    'email': metadata.get('email', ''),
                    'address': metadata.get('address', ''),
                    'billing_cycle': metadata.get('billing_cycle', 'monthly'),
                }
            )
            if not created:
                payment_obj.status = status_payment
                payment_obj.save(update_fields=['status'])
            return Response({'message': 'Webhook processed', 'status': status_payment}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error processing webhook: %s", e)
            return Response({'error': 'Internal server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
