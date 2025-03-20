# Create your views here.
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment
from .serializers import (
    CompanySubscriptionDetailsModelSerializer,
    CompanySubscriptionPlansModelsSerializer,
    PaymentSerializer
    )
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from . import helpers
from rest_framework import permissions
from helpers.payment.moyasar import Moyasar
from decouple import config
from django.contrib.auth.models import User


class CompanySubscriptionPlanViewSet(CustomBaseModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CompanySubscriptionPlansModel.objects.all()
    serializer_class = CompanySubscriptionPlansModelsSerializer


class CompanySubscriptionDetailsViewSet(CustomBaseModelViewSet):
    queryset = CompanySubscriptionDetailsModel.objects.all()
    serializer_class = CompanySubscriptionDetailsModelSerializer

    def create(self, request, *args, **kwargs):
   
    
        plan_id = request.data.get('plan')

        try:
            company_instance = request.user.company
            plan_instance = CompanySubscriptionPlansModel.objects.get(
                id=plan_id)
            subscription = helpers.create_subscription(
                company_instance, plan_instance)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        url_path="cash-and-bank-ledger", url_name="cash-and-bank-ledger",
    )
    def test(self, request, *args, **kwargs):
        return


# ========= payment APi view =========#
class PaymentCreateApiView(CreateAPIView):
    serializer_class = PaymentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

# # ======= For Development Purposes Only =======#
# class DemoPaymentApiView(APIView):
    
#     permission_classes = [permissions.AllowAny]
#     moyasar = Moyasar(config("MOYASAR_PUBLIC"), config(
#         "MOYASAR_SECRET"), "https://pwr6fhq5-8000.asse.devtunnels.ms/subscriptions/payment/process/")
#     def get(self, request):
#         payment = self.moyasar.payment(amount=9000, 
#                                        currency="SAR", 
#                                        description="Test Payment", 
#                                        metadata={"subscription_id": 2, "type": "payment", 'user_id': 1, "payed_for": "s"}, source={
#                                        "name": "demo", "number": "4111111111111111", "cvc": "123", "month": 12, "year": 2029})
#         return Response(payment, status=status.HTTP_200_OK)

# # ========= payment Status APi view =========#
class PaymentProcessingAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    moyasar = Moyasar(
        config("MOYASAR_PUBLIC"),
        config("MOYASAR_SECRET"),
        config("MOYASAR_CALLBACK_URL")
    )

 
    def post(self, request):
        payment_id = request.data.get("payment_id")
        if not payment_id:
            return Response({"message": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = self.moyasar.get_payment_by_id(payment_id)
        if not payment_status:
            return Response({"message": "Invalid payment ID or payment not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the Payment instance exists
        payment_query = Payment.objects.filter(payment_id=payment_id).first()
        if not payment_query:
            return Response({"message": "No matching payment record found"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if payment is successful
        if payment_status.get("status") == "paid":
            payment_metadata = payment_status.get("metadata", {})
            subscription_id = payment_metadata.get("subscription_id")
            user_id = payment_metadata.get("user_id")

            if not subscription_id or not user_id:
                return Response({"message": "Missing subscription or user details"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
                user = User.objects.get(pk=user_id)
                company = user.company
            except (CompanySubscriptionPlansModel.DoesNotExist, User.DoesNotExist):
                return Response({"message": "Invalid subscription or user data"}, status=status.HTTP_400_BAD_REQUEST)

            # Create or get subscription details
            subscribed_details, created = CompanySubscriptionDetailsModel.objects.get_or_create(
                company=company
            )

            if created:
                subscribed_details.payment = payment_query  
                subscribed_details.plan = subscription_plan
                
                subscribed_details.save()
            else:
                subscribed_details.payment = payment_query
                subscribed_details.plan = subscription_plan
                subscribed_details.save() 
            return Response({"message": "Payment is successful", "status": payment_status}, status=status.HTTP_200_OK)

        return Response({"message": "Payment is not successful", "status": payment_status}, status=status.HTTP_400_BAD_REQUEST)


