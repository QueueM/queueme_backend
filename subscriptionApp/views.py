"""
Advanced API views for handling subscription plans, subscription details, 
and payments. This file includes endpoints for:
  - Listing and managing Company Subscription Plans.
  - Retrieving subscription details for a company.
  - Creating or updating subscription details.
  - Creating payments (which also update the subscription).
  - Processing payment callbacks.
  - A demo endpoint for testing payments via the Moyasar gateway.
"""

import logging
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet

from .models import (
    CompanySubscriptionPlansModel,
    CompanySubscriptionDetailsModel,
    Payment
)
from .serializers import (
    CompanySubscriptionPlansModelsSerializer,
    CompanySubscriptionDetailsModelSerializer,
    PaymentSerializer
)
from . import helpers
from helpers.payment.moyasar import Moyasar
from decouple import config

# Set up a logger for this module.
logger = logging.getLogger(__name__)

# ------------------------------
# Company Subscription Plan ViewSet
# ------------------------------
class CompanySubscriptionPlanViewSet(CustomBaseModelViewSet):
    """
    Provides CRUD operations for Company Subscription Plans.
    """
    permission_classes = [permissions.AllowAny]
    queryset = CompanySubscriptionPlansModel.objects.all()
    serializer_class = CompanySubscriptionPlansModelsSerializer


# ------------------------------
# Company Subscription Plan Details API View
# ------------------------------
class CompanySubscriptionPlanDetailsAPIView(APIView):
    """
    Retrieves the subscription details for the current user’s company.
    """
    def get(self, request):
        try:
            company = request.user.company
            subscription = CompanySubscriptionDetailsModel.objects.filter(company=company).first()
            if not subscription:
                logger.info("No subscription plan exists for company ID %s", company.pk)
                return Response({"message": "No Subscription plan exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = CompanySubscriptionDetailsModelSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error retrieving company subscription plan details: %s", e)
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------
# Company Subscription Details ViewSet
# ------------------------------
class CompanySubscriptionDetailsViewSet(CustomBaseModelViewSet):
    """
    Handles creation and management of company subscription details.
    """
    queryset = CompanySubscriptionDetailsModel.objects.all()
    serializer_class = CompanySubscriptionDetailsModelSerializer

    def create(self, request, *args, **kwargs):
        """
        Create or update a subscription for the user's company.
        Expected data:
            - plan: the subscription plan ID
            - billing_cycle: "monthly" or "yearly" (defaults to "monthly")
        """
        plan_id = request.data.get('plan')
        billing_cycle = request.data.get('billing_cycle', 'monthly')
        logger.debug("Received create subscription request with plan: %s and billing_cycle: %s", plan_id, billing_cycle)

        try:
            company_instance = request.user.company
            plan_instance = CompanySubscriptionPlansModel.objects.get(id=plan_id)
        except CompanySubscriptionPlansModel.DoesNotExist:
            logger.error("Plan ID %s not found", plan_id)
            return Response({'error': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error retrieving company or plan: %s", e)
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Calculate subscription duration based on billing cycle.
        duration = plan_instance.yearly_duration_days if billing_cycle == "yearly" else plan_instance.duration_days

        # Update existing subscription or create new one.
        existing_subscription = CompanySubscriptionDetailsModel.objects.filter(company=company_instance).first()
        if existing_subscription:
            existing_subscription.plan = plan_instance
            existing_subscription.billing_cycle = billing_cycle
            existing_subscription.start_date = timezone.now()
            existing_subscription.end_date = timezone.now() + timezone.timedelta(days=duration)
            existing_subscription.save()
            logger.info("Updated subscription for company ID %s with plan ID %s", company_instance.pk, plan_id)
            serializer = self.get_serializer(existing_subscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            subscription = helpers.create_subscription(company_instance, plan_instance, billing_cycle)
            logger.info("Created new subscription for company ID %s with plan ID %s", company_instance.pk, plan_id)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="cash-and-bank-ledger")
    def test(self, request, *args, **kwargs):
        """
        Test endpoint to verify that the subscription details viewset is working.
        """
        return Response({"message": "Test successful"}, status=status.HTTP_200_OK)


# ------------------------------
# Payment Create API View (immediate subscription update)
# ------------------------------
class PaymentCreateApiView(CreateAPIView):
    """
    Handles payment creation and immediately updates the company subscription details.
    Expects payment related fields in the request payload.
    """
    permission_classes = [permissions.IsAuthenticated]  # Ensure that only authenticated users can create payments.
    serializer_class = PaymentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def create(self, request, *args, **kwargs):
        logger.info("Received payment creation request: %s", request.data)
        response = super().create(request, *args, **kwargs)
        try:
            # Extract subscription details from the request.
            subscription_id = request.data.get("subscription_id")
            billing_cycle = request.data.get("billing_cycle", "monthly")
            logger.debug("PaymentCreateApiView: subscription_id=%s, billing_cycle=%s", subscription_id, billing_cycle)

            company_instance = request.user.company
            plan_instance = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
            duration = plan_instance.yearly_duration_days if billing_cycle == "yearly" else plan_instance.duration_days

            # Update or create subscription details.
            subscription, created = CompanySubscriptionDetailsModel.objects.update_or_create(
                company=company_instance,
                defaults={
                    "plan": plan_instance,
                    "billing_cycle": billing_cycle,
                    "start_date": timezone.now(),
                    "end_date": timezone.now() + timezone.timedelta(days=duration)
                }
            )
            logger.info("Subscription updated/created for company ID %s; billing_cycle=%s, end_date=%s",
                        company_instance.pk, subscription.billing_cycle, subscription.end_date)
        except Exception as e:
            logger.exception("Error updating subscription after payment creation: %s", e)
        return response


# ------------------------------
# Demo Payment API View (for testing payment creation)
# ------------------------------
class DemoPaymentApiView(APIView):
    """
    Demo endpoint for creating a test payment via the Moyasar payment gateway.
    """
    permission_classes = [permissions.AllowAny]
    moyasar = Moyasar(
        config("MOYASAR_PUBLIC_SUBSCRIPTIONS"),
        config("MOYASAR_SECRET_SUBSCRIPTIONS"),
        "https://shop.queueme.net/user/account/billing/"
    )

    def get(self, request):
        # Use request.data.get() but note: in GET requests, you might use query parameters.
        amount = int(request.data.get("amount", 0))
        metadata = {
            "subscription_id": request.data.get("subscription_id"),
            "type": request.data.get("payment", "payment"),
            "user_id": 1,
            "payed_for": "s",
            "billing_cycle": request.data.get("billing_cycle", "monthly")
        }
        source = {
            "name": "demo",
            "number": "4111111111111111",
            "cvc": "123",
            "month": 12,
            "year": 2029
        }
        logger.info("DemoPaymentApiView: initiating demo payment with amount %s and metadata %s", amount, metadata)
        payment = self.moyasar.payment(
            amount=amount,
            description="Test Payment",
            metadata=metadata,
            source=source
        )
        return Response(payment, status=status.HTTP_200_OK)


# ------------------------------
# Payment Processing API View
# ------------------------------
class PaymentProcessingAPIView(APIView):
    """
    Endpoint for processing a payment callback, verifying the payment status via Moyasar,
    and updating the corresponding subscription details.
    """
    permission_classes = [permissions.AllowAny]
    moyasar = Moyasar(
        config("MOYASAR_PUBLIC_SUBSCRIPTIONS"),
        config("MOYASAR_SECRET_SUBSCRIPTIONS"),
        config("MOYASAR_CALLBACK_URL_SUBSCRIPTIONS")
    )

    def post(self, request):
        payment_id = request.data.get("payment_id")
        logger.info("PaymentProcessingAPIView: processing payment ID %s", payment_id)
        if not payment_id:
            return Response({"message": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = self.moyasar.get_payment_by_id(payment_id)
        if not payment_status:
            logger.error("Invalid payment ID or payment not found on Moyasar side: %s", payment_id)
            return Response({"message": "Invalid payment ID or payment not found"}, status=status.HTTP_400_BAD_REQUEST)

        payment_query = Payment.objects.filter(payment_id=payment_id).first()
        if not payment_query:
            logger.error("No matching Payment record found for payment_id: %s", payment_id)
            return Response({"message": "No matching payment record found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_query.status = payment_status.get("status")
            payment_query.save()
            logger.info("Updated Payment record with new status: %s", payment_query.status)

            if payment_status.get("status") == "paid":
                payment_metadata = payment_status.get("metadata", {})
                subscription_id = payment_metadata.get("subscription_id")
                billing_cycle = payment_metadata.get("billing_cycle", "monthly")
                user_id = payment_metadata.get("user_id")

                logger.debug("Payment metadata: subscription_id=%s, billing_cycle=%s, user_id=%s",
                             subscription_id, billing_cycle, user_id)
                if not subscription_id or not user_id:
                    return Response({"message": "Missing subscription or user details"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
                    user = User.objects.get(pk=user_id)
                    company = user.company
                except (CompanySubscriptionPlansModel.DoesNotExist, User.DoesNotExist) as e:
                    logger.error("Invalid subscription plan or user data: %s", e)
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
                    logger.info("Updated existing subscription details for company ID %s", company.pk)
                else:
                    subscribed_details = CompanySubscriptionDetailsModel.objects.create(
                        company=company,
                        plan=subscription_plan,
                        payment=payment_query,
                        billing_cycle=billing_cycle,
                        start_date=timezone.now(),
                        end_date=timezone.now() + timezone.timedelta(days=duration)
                    )
                    logger.info("Created new subscription details for company ID %s", company.pk)
                return Response({"message": "Payment is successful", "status": payment_status}, status=status.HTTP_200_OK)

            logger.warning("Payment is not successful. Payment status: %s", payment_status.get("status"))
            return Response({"message": "Payment is not successful", "status": payment_status}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Error processing payment: %s", e)
            return Response({"error": "Internal Server Error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
