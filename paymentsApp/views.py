from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(CustomBaseModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment logged successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoyasarWebhookView(APIView):
    """
    Webhook to handle Moyasar payment status updates.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        moyasar_payment_id = data.get("id")
        status_value = data.get("status")

        if not moyasar_payment_id or not status_value:
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.filter(payment_id=moyasar_payment_id).first()
        if payment:
            payment.status = status_value
            payment.save()
        else:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"message": "Webhook processed", "payment_status": status_value},
            status=status.HTTP_200_OK
        )
