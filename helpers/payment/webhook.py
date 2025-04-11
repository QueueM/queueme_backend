from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from usersapp.models import User
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

# Configure logger for debugging and traceability.
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class WebHookApiView(APIView):
    """
    Advanced Webhook API view handling callbacks from Moyasar Payment Gateway.
    Processes the payment result, validates the request payload,
    and updates subscription and payment records accordingly.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Log the incoming request data
            logger.info("Received webhook callback: %s", request.data)
            data = request.data.get("data", {})
            metadata = data.get("metadata", {})

            # Extract required fields from the callback payload.
            payment_id = data.get("id")
            status = data.get("status")
            amount = data.get("amount")
            subscription_id = metadata.get("subscription_id")
            subscription_type = metadata.get("type", "")  # "payment" for new, "upgrade" for upgrading plan
            user_id = metadata.get("user_id")
            payed_for = metadata.get("payed_for")

            # Validate that all required fields are present.
            if not all([subscription_id, subscription_type, user_id, payment_id, payed_for]):
                logger.error(
                    "Missing required fields: subscription_id: %s, subscription_type: %s, user_id: %s, payment_id: %s, payed_for: %s",
                    subscription_id, subscription_type, user_id, payment_id, payed_for
                )
                return Response({"error": "Missing required fields"}, status=400)

            # Retrieve related models.
            user = User.objects.get(pk=user_id)
            company = user.company
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)

            # Create or retrieve the Payment record.
            payment, created = Payment.objects.get_or_create(
                payment_id=payment_id,
                defaults={"amount": amount, "status": status, "payed_for": payed_for}
            )
            if not created:
                payment.status = status
                payment.amount = amount
                payment.save()

            # Only proceed if the payment has been successfully made.
            if status.lower() != "paid":
                logger.warning("Payment not completed. Payment ID: %s, Status: %s", payment_id, status)
                return Response({"error": "Payment not completed", "status": status}, status=400)

            # Retrieve or create subscription details for the given company.
            company_subscription, created = CompanySubscriptionDetailsModel.objects.get_or_create(
                company=company,
                defaults={"plan": subscription_plan, "payment": payment}
            )
            # If the subscription record exists but lacks a plan, update it.
            if not company_subscription.plan:
                company_subscription.plan = subscription_plan

            # Process the webhook based on subscription type.
            if subscription_type == "upgrade":
                # Validate if the upgrade amount is sufficient.
                if company_subscription.plan:
                    required_amount = company_subscription.have_to_pay(new_plan_price=subscription_plan.price)
                    if amount < required_amount:
                        logger.error(
                            "Insufficient amount for upgrade. Required: %s, Provided: %s", 
                            required_amount, amount
                        )
                        return Response({"error": "Insufficient amount for upgrade"}, status=400)

                company_subscription.plan = subscription_plan
                company_subscription.payment = payment
                company_subscription.save()
                logger.info("Plan upgraded successfully for company ID %s", company.pk)
                return Response({"status": status, "message": "Plan upgraded successfully"}, status=200)

            if subscription_type == "payment":
                company_subscription.payment = payment  # Associate payment record
                company_subscription.save()
                logger.info("Subscription purchased successfully for company ID %s", company.pk)
                return Response({"status": status, "message": "Subscription purchased successfully"}, status=200)

            # If the subscription type was not recognized.
            logger.error("Unhandled subscription type received: %s", subscription_type)
            return Response({"status": status, "message": "Unhandled payment status"}, status=400)

        except (User.DoesNotExist, CompanyDetailsModel.DoesNotExist,
                CompanySubscriptionPlansModel.DoesNotExist, CompanySubscriptionDetailsModel.DoesNotExist,
                Payment.DoesNotExist) as e:
            logger.error("Resource not found: %s", str(e))
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            logger.exception("Internal Server Error: %s", str(e))
            return Response({"error": "Internal Server Error", "details": str(e)}, status=500)
