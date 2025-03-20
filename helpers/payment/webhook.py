from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from usersapp.models import User
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment

@method_decorator(csrf_exempt, name='dispatch')
class WebHookApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data.get("data", {})
            metadata = data.get("metadata", {})
            payment_id = data.get("id")
            status = data.get("status")
            amount = data.get("amount")
            subscription_id = metadata.get("subscription_id")
            subscription_type = metadata.get("type", "")
            user_id = metadata.get("user_id")
            payed_for = metadata.get("payed_for")

            if not all([subscription_id, subscription_type, user_id, payment_id, payed_for]):
                return Response({"error": "Missing required fields"}, status=400)

            user = User.objects.get(pk=user_id)
            company = user.company
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
            payment = Payment.objects.get(payment_id=payment_id)
            payment.status = status         
            payment.save()
            if status == "paid":        
                company_subscription, _ = CompanySubscriptionDetailsModel.objects.get_or_create(company=company)
                if subscription_type == "upgrade" and amount == company_subscription.have_to_pay(new_plan_price=subscription_plan.price):
                    company_subscription.plan= subscription_plan
                    company_subscription.payment = payment
                    company_subscription.save()
                    return Response({"status": status, "message": "Plan upgraded successfully"}, status=200)
                
                if subscription_type == "payment":
                    company_subscription ,  created = CompanySubscriptionDetailsModel.objects.get_or_create(plan=subscription_plan, company=company)
                    if created:
                        company_subscription.payment = payment
                        company_subscription.save()
                    
                    return Response({"status": status, "message": "Purchase successful"}, status=200)
            return Response({"status": status, "message": "Unhandled payment status"}, status=400)

        except (User.DoesNotExist, CompanyDetailsModel.DoesNotExist, CompanySubscriptionPlansModel.DoesNotExist, 
                CompanySubscriptionDetailsModel.DoesNotExist, Payment.DoesNotExist) as e:
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": "Internal Server Error", "details": str(e)}, status=500)