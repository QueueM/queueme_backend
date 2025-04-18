from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import EmployeeDetailsModel, EmployeeRoleManangementModel
from .serializers import EmployeeDetailsSerializer, EmployeeRoleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Helper functions for safe access can be added if needed.
def get_user_company(user):
    try:
        return user.company
    except Exception:
        return None

def get_user_employee(user):
    try:
        return user.employee
    except Exception:
        return None

class EmployeeDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeDetailsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # Optionally add filterset_class if desired.

class EmployeeRoleDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeRoleManangementModel.objects.all()
    serializer_class = EmployeeRoleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # Optionally add a filterset_class if available.

    def get_queryset(self):
        user = self.request.user
        company = get_user_company(user)
        if company:
            from shopApp.models import ShopDetailsModel
            shops = ShopDetailsModel.objects.filter(company=company)
            return EmployeeRoleManangementModel.objects.filter(shop__in=shops)
        else:
            employee = get_user_employee(user)
            if employee:
                assigned_roles = EmployeeRoleManangementModel.objects.filter(employee=employee)
                return assigned_roles
        return EmployeeRoleManangementModel.objects.none()
