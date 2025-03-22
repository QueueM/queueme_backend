from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from usersapp.models import User
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment
from rest_framework.response import Response
from rest_framework.views import APIView

@method_decorator(csrf_exempt, name='dispatch')
class WebHookApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get("data", {})
            metadata = data.get("metadata", {})

            # Extract required fields
            payment_id = data.get("id")
            status = data.get("status") 
            amount = data.get("amount")
            subscription_id = metadata.get("subscription_id")
            subscription_type = metadata.get("type", "")
            user_id = metadata.get("user_id")
            payed_for = metadata.get("payed_for")

            # Validate required fields
            if not all([subscription_id, subscription_type, user_id, payment_id, payed_for]):
                return Response({"error": "Missing required fields"}, status=400)

            # Retrieve User, Company, and Subscription Plan
            user = User.objects.get(pk=user_id)
            company = user.company
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)

            # Create or retrieve payment record
            payment, created = Payment.objects.get_or_create(
                payment_id=payment_id,
                defaults={"amount": amount, "status": status, "payed_for": payed_for}
            )
            if not created:
                payment.status = status
                payment.amount = amount
                payment.save()

            # Ensure payment is **paid** before proceeding
            if status.lower() != "paid":
                return Response({"error": "Payment not completed", "status": status}, status=400)

            # Retrieve or create subscription details
            company_subscription, created = CompanySubscriptionDetailsModel.objects.get_or_create(
                company=company,
                defaults={"plan": subscription_plan, "payment": payment}
            )

            # If the subscription exists but has no plan, assign it
            if not company_subscription.plan:
                company_subscription.plan = subscription_plan

            # Handle subscription upgrade
            if subscription_type == "upgrade":
                if company_subscription.plan:
                    required_amount = company_subscription.have_to_pay(new_plan_price=subscription_plan.price)
                    if amount < required_amount:
                        return Response({"error": "Insufficient amount for upgrade"}, status=400)

                company_subscription.plan = subscription_plan
                company_subscription.payment = payment
                company_subscription.save()
                return Response({"status": status, "message": "Plan upgraded successfully"}, status=200)

            # Handle new subscription purchase
            if subscription_type == "payment":
                if created:
                    company_subscription.payment = payment
                    company_subscription.save()
                return Response({"status": status, "message": "Subscription purchased successfully"}, status=200)

            return Response({"status": status, "message": "Unhandled payment status"}, status=400)

        except (User.DoesNotExist, CompanyDetailsModel.DoesNotExist, CompanySubscriptionPlansModel.DoesNotExist,
                CompanySubscriptionDetailsModel.DoesNotExist, Payment.DoesNotExist) as e:
            
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": "Internal Server Error", "details": str(e)}, status=500)
