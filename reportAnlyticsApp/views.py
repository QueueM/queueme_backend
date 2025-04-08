from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Max, Min, Sum

from shopApp.models import ShopDetailsModel
from shopServiceApp.models import ShopServiceDetailsModel, ServiceBookingDetailsModel
from customersApp.models import CustomersDetailsModel
from employeeApp.models import EmployeeDetailsModel
from adsApp.models import ShopAdsModel, ShopAdsImpressionModel
from reelsApp.models import ReelsModel
from chatApp.models import ChatRoomModel
from companyApp.models import CompanyDetailsModel


def get_fields(request):
    fields_param = request.query_params.get("fields")
    if fields_param:
        fields = [field.strip() for field in fields_param.split(",") if field.strip()]
    else:
        fields = []
    return fields


def get_shop(request):
    shop_id = request.query_params.get("shop_id")
    if shop_id:
        shop = ShopDetailsModel.objects.filter(owner=request.user, id=shop_id)
    else:
        company = CompanyDetailsModel.objects.filter(user=request.user).prefetch_related("shops").first()
        shop = company.shops.all() if company else ShopDetailsModel.objects.none()
        print("company_shop",shop)
    return shop


class CustomerReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fields = get_fields(request)
        result = {}
        try:
            customer = CustomersDetailsModel.objects
            if not fields or "total_customers" in fields:
                result["total_customers"] = customer.count()
            if "customer_gender_count" in fields:
                result["customer_gender_count"] = list(
                    customer.values("gender").annotate(count=Count("id"))
                )
            if "customer_type_count" in fields:
                result["customer_type_count"] = list(
                    customer.values("customer_type")
                    .annotate(count=Count("id"))
                    .order_by("customer_type")
                )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShopReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields = get_fields(request)
        result = {}

        try:
            qs = ShopDetailsModel.objects.filter(owner=request.user)

            if not fields or "total_shops" in fields:
                result["total_shops"] = qs.count()

            # if not fields or "active_vs_inactive" in fields:
            #     result["active_vs_inactive"] = {
            #         "active": qs.filter(is_active=True).count(),
            #         "inactive": qs.filter(is_active=False).count()
            #     }



            if "shop_locations" in fields:
                result["city"] = list(
                    qs.values("city")
                    .annotate(count=Count("id"))
                    .order_by("city")
                )

            # if not fields or "created_dates" in fields:
            #     result["created_dates"] = list(
            #         qs.values("id", "name", "created_at").order_by("-created_at")
            #     )

            if "by_customer_type" in fields:
                result["by_customer_type"] = list(
                    qs.values("customers_type")
                    .annotate(count=Count("id"))
                    .order_by("customers_type")
                )

            if "by_service_type" in fields:
                result["by_service_type"] = list(
                    qs.values("services_types")
                    .annotate(count=Count("id"))
                    .order_by("services_types")
                )

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}
            shop = get_shop(request)

            if not shop.exists():
                return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

            if not fields or "total_services" in fields:
                result["total_services"] = ShopServiceDetailsModel.objects.filter(shop__in=shop).count()

            if "available_services" in fields:
                result["available_services"] = ShopServiceDetailsModel.objects.filter(
                    is_availabe=True, shop__in=shop
                ).count()

            if "services_by_type" in fields:
                result["services_by_type"] = list(
                    ShopServiceDetailsModel.objects.filter(shop__in=shop)
                    .values("service_type")
                    .annotate(count=Count("id"))
                    .order_by("service_type")
                )

            if "price_statistics" in fields:
                price_stats = ShopServiceDetailsModel.objects.filter(shop__in=shop).aggregate(
                    min_price=Min("price"),
                    max_price=Max("price"),
                    avg_price=Avg("price"),
                )
                result["price_statistics"] = {
                    "min_price": price_stats["min_price"] or 0,
                    "max_price": price_stats["max_price"] or 0,
                    "avg_price": round(price_stats["avg_price"], 2) if price_stats["avg_price"] else 0,
                }

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceBookingReportApiView(APIView):
    permission_classes = [IsAuthenticated]
    # filter based on shop
    def get(self, request, *args, **kwargs):
        try:
            fields = get_fields(request)
            result = {}

            if not fields or "total_bookings" in fields:
                result["total_bookings"] = ServiceBookingDetailsModel.objects.filter(user=request.user).count()

            if "bookings_by_status" in fields:
                result["bookings_by_status"] = list(
                    ServiceBookingDetailsModel.objects.filter(user=request.user)
                    .values("status")
                    .annotate(count=Count("id"))
                    .order_by("status")
                )

            if "revenue_statistics" in fields:
                revenue_stats = ServiceBookingDetailsModel.objects.filter(user=request.user).aggregate(
                    min_final_amount=Min("final_amount"),
                    max_final_amount=Max("final_amount"),
                    avg_final_amount=Avg("final_amount"),
                )
                result["revenue_statistics"] = {
                    "min_final_amount": revenue_stats["min_final_amount"] or 0,
                    "max_final_amount": revenue_stats["max_final_amount"] or 0,
                    "avg_final_amount": round(revenue_stats["avg_final_amount"], 2) if revenue_stats["avg_final_amount"] else 0,
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
            shop = get_shop(request)

            if not shop.exists():
                return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

            if not fields or "total_employees" in fields:
                result["total_employees"] = EmployeeDetailsModel.objects.filter(shop__in=shop).count()

            if "employees_by_role" in fields:
                result["employees_by_role"] = list(
                    EmployeeDetailsModel.objects.filter(shop__in=shop)
                    .values("roles")
                    .annotate(count=Count("id"))
                    .order_by("roles")
                )

            if "salary_statistics" in fields:
                salary_stats = EmployeeDetailsModel.objects.filter(shop__in=shop).aggregate(
                    min_salary=Min("salary"),
                    max_salary=Max("salary"),
                    avg_salary=Avg("salary"),
                )
                result["salary_statistics"] = {
                    "min_salary": salary_stats["min_salary"] or 0,
                    "max_salary": salary_stats["max_salary"] or 0,
                    "avg_salary": round(salary_stats["avg_salary"], 2) if salary_stats["avg_salary"] else 0,
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
            shop = get_shop(request)

            if not shop.exists():
                return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

            if not fields or "total_ads" in fields:
                result["total_ads"] = ShopAdsModel.objects.filter(shop__in=shop).count()

            if "ads_by_gender" in fields:
                result["ads_by_gender"] = list(
                    ShopAdsModel.objects.filter(shop__in=shop)
                    .values("target_gender")
                    .annotate(count=Count("id"))
                    .order_by("target_gender")
                )

            if "ads_performance" in fields:
                total_clicks = ShopAdsImpressionModel.objects.filter(ad__shop__in=shop).count()
                total_impressions = total_clicks
                total_spend = total_clicks  # assuming cost per click = 1
                average_ctr = round(total_clicks / total_impressions, 2) if total_impressions > 0 else 0

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
        shop = get_shop(request)

        if not shop.exists():
            return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            if not fields or "total_reels" in fields:
                result["total_reels"] = ReelsModel.objects.filter(shop__in=shop).count()

            if "reels_likes_count" in fields:
                result["reels_likes_count"] = ReelsModel.objects.filter(shop__in=shop).aggregate(
                    total_likes=Count("likes")
                )["total_likes"] or 0

            if "reels_comments_count" in fields:
                result["reels_comments_count"] = ReelsModel.objects.filter(shop__in=shop).aggregate(
                    total_comments=Count("comments")
                )["total_comments"] or 0

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChatReportApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fields = get_fields(request)
        result = {}
        try:
            shop = get_shop(request)

            if not shop.exists():
                return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)

            if not fields or "total_chats" in fields:
                result["total_chats"] = ChatRoomModel.objects.filter(shop__in=shop).count()

            if "chats_by_shop" in fields:
                result["chats_by_shop"] = list(
                    ChatRoomModel.objects.filter(shop__in=shop)
                    .values("shop__name")
                    .annotate(count=Count("id"))
                    .order_by("shop__name")
                )

            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
