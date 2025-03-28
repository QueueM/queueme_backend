from  rest_framework.viewsets import ViewSet
from  rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework.decorators import action
from  rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q , F ,Sum,Count,Avg,Max,Min,Subquery,OuterRef,Case,When
# All Models Will be here
from customersApp.models import CustomersDetailsModel
from companyApp.models import CompanyDetailsModel
from  shopApp.models import ShopDetailsModel



# class CustomersReportApiViewSet(ViewSet):
#     permission_classes = [IsAuthenticated]  
#     @action(detail=False, methods=['get'])
#     def total_customers(self, request):
#         try:
#             total_customers = CustomersDetailsModel.objects.count()
#             return Response({"total_customers": total_customers}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     @action(detail=False, methods=['get'])
#     def gender_count(self, request):
#         try:
#             male_count = CustomersDetailsModel.objects.filter(gender="male").count()
#             female_count = CustomersDetailsModel.objects.filter(gender="female").count()
#             return Response({"male": male_count, "female": female_count}, status=status.HTTP_200_OK)
#         except Exception as e:  
                
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     @action(detail=False, methods=['get'])
#     def customer_type_count(self, request):
#         try:
#             regular = CustomersDetailsModel.objects.filter(customer_type="regular").count()
#             vip = CustomersDetailsModel.objects.filter(customer_type="vip").count()
#             new_customer = CustomersDetailsModel.objects.filter(customer_type="new_customer").count()
#             return Response({
#                 "regular": regular, 
#                 "vip": vip, 
#                 "new_customer": new_customer
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShopReportApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        fields_param = request.query_params.get('fields')
        if fields_param:
            fields = [field.strip() for field in fields_param.split(",") if field.strip()]
            print("Requested report fields:", fields)
        else:
            fields = []
        
        report = {}      
        try:
            if not fields or "total_shops" in fields:
                report["total_shops"] = ShopDetailsModel.objects.filter(owner = request.user).count()
            
            if "by_customer_type" in fields:
                by_customer_type = ShopDetailsModel.objects.filter(owner = request.user).values("customers_type")\
                                      .annotate(count=Count("id"))\
                                    .order_by("customers_type")
    
                report["by_customer_type"] = list(by_customer_type)
            
            if "by_service_type" in fields:
                by_service_type = ShopDetailsModel.objects.filter(owner = request.user).values("services_types")\
                                    .annotate(count=Count("id"))\
                                    .order_by("services_types")
                report["by_service_type"] = list(by_service_type)
            
            return Response(report, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   