from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment
from .serializers import (
    CompanySubscriptionDetailsModelSerializer,
    CompanySubscriptionPlansModelsSerializer,
    PaymentSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from . import helpers
from helpers.payment.moyasar import Moyasar
from decouple import config
from django.contrib.auth.models import User
from django.utils import timezone

# ------------------------------
# Company Subscription Plan ViewSet
# ------------------------------
class CompanySubscriptionPlanViewSet(CustomBaseModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = CompanySubscriptionPlansModel.objects.all()
    serializer_class = CompanySubscriptionPlansModelsSerializer

# ------------------------------
# Company Subscription Plan Details API View
# ------------------------------
class CompanySubscriptionPlanDetailsAPIView(APIView):
    def get(self, request):
        obj = CompanySubscriptionDetailsModel.objects.filter(company=request.user.company)
        if not obj.exists():
            return Response({"message": "No Subscription plan exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CompanySubscriptionDetailsModelSerializer(obj.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------
# Company Subscription Details ViewSet
# ------------------------------
class CompanySubscriptionDetailsViewSet(CustomBaseModelViewSet):
    queryset = CompanySubscriptionDetailsModel.objects.all()
    serializer_class = CompanySubscriptionDetailsModelSerializer

    def create(self, request, *args, **kwargs):
        plan_id = request.data.get('plan')
        billing_cycle = request.data.get('billing_cycle', 'monthly')
        print("DEBUG: Received plan from request:", plan_id)
        print("DEBUG: Received billing_cycle from request:", billing_cycle)

        try:
            company_instance = request.user.company
            plan_instance = CompanySubscriptionPlansModel.objects.get(id=plan_id)
        except CompanySubscriptionPlansModel.DoesNotExist:
            return Response({'error': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update existing subscription or create a new one
        existing_subscription = CompanySubscriptionDetailsModel.objects.filter(company=company_instance).first()
        duration = plan_instance.yearly_duration_days if billing_cycle == "yearly" else plan_instance.duration_days
        if existing_subscription:
            existing_subscription.plan = plan_instance
            existing_subscription.billing_cycle = billing_cycle
            existing_subscription.start_date = timezone.now()
            existing_subscription.end_date = timezone.now() + timezone.timedelta(days=duration)
            existing_subscription.save()
            serializer = self.get_serializer(existing_subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            subscription = helpers.create_subscription(company_instance, plan_instance, billing_cycle)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="cash-and-bank-ledger")
    def test(self, request, *args, **kwargs):
        return Response({"message": "Test successful"}, status=status.HTTP_200_OK)

# ------------------------------
# Payment Create API View (Option B: immediate subscription update)
# ------------------------------
class PaymentCreateApiView(CreateAPIView):
    serializer_class = PaymentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        # Log the incoming payment data
        print("DEBUG: PaymentCreateApiView data:", request.data)
        # Create the Payment record using the serializer
        response = super().create(request, *args, **kwargs)

        try:
            # Extract subscription info from the request
            subscription_id = request.data.get("subscription_id")
            billing_cycle = request.data.get("billing_cycle", "monthly")
            print("DEBUG: subscription_id:", subscription_id)
            print("DEBUG: billing_cycle:", billing_cycle)
            
            company_instance = request.user.company
            # Here subscription_id corresponds to the plan's ID
            plan_instance = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
            duration = plan_instance.yearly_duration_days if billing_cycle == "yearly" else plan_instance.duration_days

            # Update existing subscription or create a new one for this company
            subscription, created = CompanySubscriptionDetailsModel.objects.update_or_create(
                company=company_instance,
                defaults={
                    "plan": plan_instance,
                    "billing_cycle": billing_cycle,
                    "start_date": timezone.now(),
                    "end_date": timezone.now() + timezone.timedelta(days=duration)
                }
            )
            print("DEBUG: Subscription updated. Billing cycle:", subscription.billing_cycle, "End date:", subscription.end_date)
        except Exception as e:
            print("DEBUG: Error updating subscription:", str(e))
        
        return response

# ------------------------------
# Demo Payment API View (for testing payment creation)
# ------------------------------
class DemoPaymentApiView(APIView):
    permission_classes = [permissions.AllowAny]
    moyasar = Moyasar(
        config("MOYASAR_PUBLIC"), 
        config("MOYASAR_SECRET"), 
        "https://pwr6fhq5-8000.asse.devtunnels.ms/subscriptions/payment/process/"
    )

    def get(self, request):
        payment = self.moyasar.payment(
            amount=int(request.data.get("amount", 0)),
            currency="SAR",
            description="Test Payment",
            metadata={
                "subscription_id": request.data.get("subscription_id"),
                "type": request.data.get("payment", "payment"),
                "user_id": 1,
                "payed_for": "s",
                "billing_cycle": request.data.get("billing_cycle", "monthly")  # ensure billing_cycle is sent
            },
            source={
                "name": "demo",
                "number": "4111111111111111",
                "cvc": "123",
                "month": 12,
                "year": 2029
            }
        )
        return Response(payment, status=status.HTTP_200_OK)

# ------------------------------
# Payment Processing API View
# ------------------------------
class PaymentProcessingAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    moyasar = Moyasar(
        config("MOYASAR_PUBLIC"),
        config("MOYASAR_SECRET"),
        config("MOYASAR_CALLBACK_URL")
    )

    def post(self, request):
        payment_id = request.data.get("payment_id")
        print("DEBUG: Payment ID from request:", payment_id)
        if not payment_id:
            return Response({"message": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = self.moyasar.get_payment_by_id(payment_id)
        if not payment_status:
            return Response({"message": "Invalid payment ID or payment not found"}, status=status.HTTP_400_BAD_REQUEST)

        payment_query = Payment.objects.filter(payment_id=payment_id).first()
        if not payment_query:
            return Response({"message": "No matching payment record found"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.get(payment_id=payment_id)
        payment.status = payment_status.get("status")
        payment.save()

        if payment_status.get("status") == "paid":
            payment_metadata = payment_status.get("metadata", {})
            subscription_id = payment_metadata.get("subscription_id")
            billing_cycle = payment_metadata.get("billing_cycle", "monthly")
            print("DEBUG: Payment metadata subscription_id:", subscription_id)
            print("DEBUG: Billing cycle:", billing_cycle)
            user_id = payment_metadata.get("user_id")

            if not subscription_id or not user_id:
                return Response({"message": "Missing subscription or user details"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
                user = User.objects.get(pk=user_id)
                company = user.company
            except (CompanySubscriptionPlansModel.DoesNotExist, User.DoesNotExist):
                return Response({"message": "Invalid subscription or user data"}, status=status.HTTP_400_BAD_REQUEST)

            duration = subscription_plan.yearly_duration_days if billing_cycle == "yearly" else subscription_plan.duration_days

            subscribed_details = CompanySubscriptionDetailsModel.objects.filter(company=company).first()
            if subscribed_details:
                subscribed_details.plan = subscription_plan
                subscribed_details.payment = payment_query
                subscribed_details.billing_cycle = billing_cycle
                subscribed_details.start_date = timezone.now()
                subscribed_details.end_date = timezone.now() + timezone.timedelta(days=duration)
                subscribed_details.save()
            else:
                subscribed_details = CompanySubscriptionDetailsModel.objects.create(
                    company=company,
                    plan=subscription_plan,
                    payment=payment_query,
                    billing_cycle=billing_cycle,
                    start_date=timezone.now(),
                    end_date=timezone.now() + timezone.timedelta(days=duration)
                )
            return Response({"message": "Payment is successful", "status": payment_status}, status=status.HTTP_200_OK)

        return Response({"message": "Payment is not successful", "status": payment_status}, status=status.HTTP_400_BAD_REQUEST)
