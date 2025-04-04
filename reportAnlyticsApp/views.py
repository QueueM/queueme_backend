from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Max, Min, Sum, F
from shopApp.models import ShopDetailsModel
from shopServiceApp.models import ShopServiceDetailsModel, ServiceBookingDetailsModel
from  customersApp.models import CustomersDetailsModel
from employeeApp.models import EmployeeDetailsModel
from adsApp.models import ShopAdsModel, ShopAdsImpressionModel
from reelsApp.models import ReelsModel
from chatApp.models import ChatRoomModel


def get_fields(request):
    fields_param = request.query_params.get("fields")
    if fields_param:
        fields = [field.strip()
                  for field in fields_param.split(",") if field.strip()]
        print("Requested report fields:", fields)
    else:
        fields = []
    return fields


class CustomerReportApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        fields = get_fields(request)
        result = {}
        try:
          customer = CustomersDetailsModel.objects
          if not fields or "total_customers" in fields:
            result["total_customers"] = customer.count()
          if  "customer_gender_count" in fields:
              result["customer_gender_count"] = customer.values("gender").annotate(count=Count("id"))
          if "customer_type_count" in fields:
                result["customer_type_count"] = customer.values("customer_type").annotate(count=Count("id")).order_by("customer_type")
          return Response(result, status=status.HTTP_200_OK)
          
        except CustomersDetailsModel.DoesNotExist:
          return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ShopReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if 'filters' parameter is provided and equals 'id'
        filters = request.query_params.get("filters")
        if filters != "id":
            return Response(
                {"error": "Invalid filters parameter. Expected 'id'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fields = get_fields(request)
        report = {}
        try:
            if not fields or "total_shops" in fields:
                report["total_shops"] = ShopDetailsModel.objects.filter(
                    owner=request.user
                ).count()

            if "by_customer_type" in fields:
                by_customer_type = (
                    ShopDetailsModel.objects.filter(owner=request.user)
                    .values("customers_type")
                    .annotate(count=Count("id"))
                    .order_by("customers_type")
                )
                report["by_customer_type"] = list(by_customer_type)

            if "by_service_type" in fields:
                by_service_type = (
                    ShopDetailsModel.objects.filter(owner=request.user)
                    .values("services_types")
                    .annotate(count=Count("id"))
                    .order_by("services_types")
                )
                report["by_service_type"] = list(by_service_type)

            return Response(report, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
class ServiceReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}
            shop = ShopDetailsModel.objects.filter(owner=request.user).first()

            if not shop:
                return Response(
                    {"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if not fields or "total_service" in fields:
                result["total_services"] = ShopServiceDetailsModel.objects.filter(
                    shop=shop
                ).count()

            if "available_services" in fields:
                result["available_services"] = ShopServiceDetailsModel.objects.filter(
                    is_availabe=True, shop=shop
                ).count()

            if "services_by_type" in fields:
                result["services_by_type"] = (
                    ShopServiceDetailsModel.objects.filter(shop=shop)
                    .values("service_type")
                    .annotate(count=Count("id"))
                    .order_by("service_type")
                )

            if "price_statistics" in fields:
                price_stats = ShopServiceDetailsModel.objects.filter(
                    shop=shop
                ).aggregate(
                    min_price=Min("price"),
                    max_price=Max("price"),
                    avg_price=Avg("price"),
                )
                result["price_statistics"] = {
                    "min_price": price_stats["min_price"] or 0,
                    "max_price": price_stats["max_price"] or 0,
                    "avg_price": round(price_stats["avg_price"], 2)
                    if price_stats["avg_price"]
                    else 0,
                }

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceBookingReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}

            if not fields or "total_bookings" in fields:
                result["total_bookings"] = ServiceBookingDetailsModel.objects.filter(
                    user=request.user
                ).count()

            if "bookings_by_status" in fields:
                result["bookings_by_status"] = list(
                    ServiceBookingDetailsModel.objects.filter(
                        user=request.user)
                    .values("status")
                    .annotate(count=Count("id"))
                    .order_by("status")
                )

            if "revenue_statistics" in fields:
                revenue_stats = ServiceBookingDetailsModel.objects.filter(
                    user=request.user
                ).aggregate(
                    min_final_amount=Min("final_amount"),
                    max_final_amount=Max("final_amount"),
                    avg_final_amount=Avg("final_amount"),
                )
                result["revenue_statistics"] = {
                    "min_final_amount": revenue_stats["min_final_amount"] or 0,
                    "max_final_amount": revenue_stats["max_final_amount"] or 0,
                    "avg_final_amount": round(revenue_stats["avg_final_amount"], 2)
                    if revenue_stats["avg_final_amount"]
                    else 0,
                }

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}
            shop = ShopDetailsModel.objects.filter(owner=request.user).first()

            if not shop:
                return Response(
                    {"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if not fields or "total_employees" in fields:
                result["total_employees"] = EmployeeDetailsModel.objects.filter(
                    shop=shop
                ).count()

            if "employees_by_role" in fields:
                result["employees_by_role"] = (
                    EmployeeDetailsModel.objects.filter(shop=shop)
                    .values("roles")
                    .annotate(count=Count("id"))
                    .order_by("roles")
                )

            if "salary_statistics" in fields:
                salary_stats = EmployeeDetailsModel.objects.filter(shop=shop).aggregate(
                    min_salary=Min("salary"),
                    max_salary=Max("salary"),
                    avg_salary=Avg("salary"),
                )
                result["salary_statistics"] = {
                    "min_salary": salary_stats["min_salary"] or 0,
                    "max_salary": salary_stats["max_salary"] or 0,
                    "avg_salary": round(salary_stats["avg_salary"], 2)
                    if salary_stats["avg_salary"]
                    else 0,
                }

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MarketingReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}

  
            shop = ShopDetailsModel.objects.filter(owner=request.user).first()
            if not shop:
                return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND) 
            if not fields or "total_ads" in fields:
                result["total_ads"] = ShopAdsModel.objects.filter(
                    shop=shop).count()            
            if "ads_by_gender" in fields:
                result["ads_by_gender"] = list(
                    ShopAdsModel.objects.filter(shop=shop)
                    .values("target_gender")
                    .annotate(count=Count("id"))
                    .order_by("target_gender")
                )
            if "ads_performance" in fields:
            
                total_clicks = ShopAdsImpressionModel.objects.filter(
                    ad__shop=shop).count()

                total_spend = total_clicks

                total_impressions = total_clicks
                average_ctr = 0
                if total_impressions > 0:
                    average_ctr = round(total_clicks / total_impressions, 2)

                result["ads_performance"] = {
                    "total_clicks": total_clicks,
                    "total_impressions": total_impressions,
                    "total_spend": total_spend,
                    "average_ctr": average_ctr,
                }

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ReelsReportApiVIew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fields = get_fields(request)
        result = {}
        shop = ShopDetailsModel.objects.filter(owner=request.user).first()
        if not shop:
            return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            if not fields or "total_reels" in fields:
                result["total_reels"] = ReelsModel.objects.filter(
                    shop=shop).count()
            if "reels_likes_count" in fields:
                result["reels_likes_count"] = ReelsModel.objects.filter(shop=shop).select_related("likes").aggregate(
                    total_likes=Count("likes")
                )["total_likes"]
            if "reels_comments_count" in fields:
                result["reels_comments_count"] = ReelsModel.objects.filter(shop=shop).select_related("comments").aggregate(
                    total_comments=Count("comments")
                )["total_comments"]
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ChatReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fields = get_fields(request)
        result = {}
        try:
            shop = ShopDetailsModel.objects.filter(owner=request.user).first()
            if not shop:
                return Response(
                    {"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND
                )
            if not fields or "total_chats" in fields:
                result["total_chats"] = ChatRoomModel.objects.filter(
                  shop=shop
                ).count()

            if "chats_by_shop" in fields:
                result["chats_by_shop"] = list(
                    ChatRoomModel.objects.filter(shop=shop)
                    .values("shop__name")
                    .annotate(count=Count("id"))
                    .order_by("shop__name")
                )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)