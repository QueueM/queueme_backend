from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from usersapp.models import User
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel
import json


@method_decorator(csrf_exempt, name='dispatch')
class WebHookApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data  
            print("Data" , data)
            print("Payment ID:", data.get("id"))
            print("Metadata:", data.get("data").get("metadata"))

            payment_id = data.get("id")
            status = data.get("data").get("status")
            amount = data.get("data").get("amount")
            metadata = data.get("data").get("metadata")

            subscription_id = metadata.get("subscription_id")
            subscription_type = metadata.get("type","")
            user_id = metadata.get("user_id")

         

            if not all([subscription_id, subscription_type, user_id, payment_id]):
                return Response({"error": "Missing required fields"}, status=400)

            user = User.objects.get(pk=user_id)
            company = CompanyDetailsModel.objects.get(user=user)
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)

            if status == "paid":
                if subscription_type == "upgrade":
                    company_subscription = CompanySubscriptionDetailsModel.objects.get(company=company)
                    if amount == company_subscription.have_to_pay(new_plan_price=subscription_plan.price):
                        company_subscription.plan = subscription_plan
                        company_subscription.save()
                        return Response({"status": status, "message": "Plan upgraded successfully"}, status=200)

                elif subscription_type == "payment":
                    CompanySubscriptionDetailsModel.objects.create(
                        plan=subscription_plan,
                        company=company,
                    )
                    return Response({"status": status, "message": "Purchase successful"}, status=200)

            return Response({"status": status, "message": "Unhandled payment status"}, status=400)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        except CompanyDetailsModel.DoesNotExist:
            return Response({"error": "Company not found"}, status=404)
        except CompanySubscriptionPlansModel.DoesNotExist:
            return Response({"error": "Subscription plan not found"}, status=404)
        except CompanySubscriptionDetailsModel.DoesNotExist:
            return Response({"error": "Company subscription details not found"}, status=404)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON payload"}, status=400)
        except Exception as e:
            print(str(e))
            return Response({"error": "Internal Server Error", "details": str(e)}, status=500)

