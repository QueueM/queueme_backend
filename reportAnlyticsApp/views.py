from  rest_framework.viewsets import ModelViewSet , ViewSet
from  rest_framework.response import Response
from rest_framework.decorators import action
from  rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q , F ,Sum,Count,Avg,Max,Min,Subquery,OuterRef,Case,When
# All Models Will be here
from customersApp.models import CustomersDetailsModel
from companyApp.models import CompanyDetailsModel



class CustomersReportApiViewSet(ViewSet):
    
    @action(detail=False, methods=['get'])
    def total_customers(self, request):
        total_customers = CustomersDetailsModel.objects.count()
        return Response({"total_customers": total_customers}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def gender_count(self, request):
        male_count = CustomersDetailsModel.objects.filter(gender="male").count()
        female_count = CustomersDetailsModel.objects.filter(gender="female").count()
        return Response({"male": male_count, "female": female_count}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def customer_type_count(self, request):
        regular = CustomersDetailsModel.objects.filter(customer_type="regular").count()
        vip = CustomersDetailsModel.objects.filter(customer_type="vip").count()
        new_customer = CustomersDetailsModel.objects.filter(customer_type="new_customer").count()
        return Response({
            "regular": regular, 
            "vip": vip, 
            "new_customer": new_customer
        }, status=status.HTTP_200_OK)


