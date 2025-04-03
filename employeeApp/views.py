from django.shortcuts import render

# Create your views here.



from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import EmployeeDetailsModel
from .serializers import EmployeeDetailsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import EmployeeDetailsFilter, EmployeeRoleFilter
from .models import EmployeeRoleManangementModel
from .serializers import EmployeeRoleSerializer
from shopApp.models import ShopDetailsModel
class EmployeeDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeDetailsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeDetailsFilter

class EmployeeRoleDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeRoleManangementModel.objects.all()
    serializer_class = EmployeeRoleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeRoleFilter

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company'):
            shops = ShopDetailsModel.objects.filter(company=user.company)
            return EmployeeRoleManangementModel.objects.filter(shop__in=shops)
        elif hasattr(user, 'employee'):
            assigned_roles = EmployeeRoleManangementModel.objects.filter(employee=user.employee)
            assigned_shops = ShopDetailsModel.objects.filter(id__in=assigned_roles.values_list('shop_id', flat=True))
            return EmployeeRoleManangementModel.objects.filter(shop__in=assigned_shops)
        return EmployeeRoleManangementModel.objects.none()
        


        

