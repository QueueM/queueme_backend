from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeDetailsViewset, EmployeeRoleDetailsViewset

router = DefaultRouter()
router.register(r'employees', EmployeeDetailsViewset)
router.register(r'employees-roles', EmployeeRoleDetailsViewset)

urlpatterns = [
    path('', include(router.urls)),
]
