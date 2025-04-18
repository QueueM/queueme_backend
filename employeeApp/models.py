# employeeApp/models.py

from django.db import models
from django.contrib.auth import get_user_model
from shopApp.models import ShopDetailsModel
from companyApp.models import CompanyDetailsModel
from django.utils import timezone

# Get the current user model
User = get_user_model()

def get_default_user():
    """
    Returns the primary key of the first available User.
    Make sure that at least one User exists.
    """
    default_user = User.objects.first()
    if default_user:
        return default_user.pk
    return 1  # Fallback value; ensure that a User with pk=1 exists

def get_default_company():
    """
    Returns the primary key of the first available CompanyDetailsModel.
    Ensure at least one CompanyDetailsModel exists.
    """
    default_company = CompanyDetailsModel.objects.first()
    if default_company:
        return default_company.pk
    return 1  # Fallback value; ensure that a Company with pk=1 exists

class EmployeeDetailsModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee",
        default=get_default_user  # Provide default for existing rows
    )
    company = models.ForeignKey(
        CompanyDetailsModel,
        on_delete=models.CASCADE,
        related_name="employees",
        default=get_default_company  # Provide default for existing rows
    )
    shop = models.ForeignKey(
        ShopDetailsModel,
        on_delete=models.CASCADE,
        related_name="employees"
    )
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100, default="Employee")
    salary = models.FloatField(default=0.0)
    ai_performance_data = models.JSONField(
        blank=True,
        null=True,
        help_text="AI performance analysis data",
        verbose_name="AI Performance Data"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

class EmployeeWorkingHoursModel(models.Model):
    employee = models.ForeignKey(EmployeeDetailsModel, on_delete=models.CASCADE, related_name="working_hours")
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.name} - {self.day}"

def get_default_employee_pk():
    """
    Returns the primary key of the first available EmployeeDetailsModel.
    Ensure that at least one EmployeeDetailsModel exists.
    """
    default_employee = EmployeeDetailsModel.objects.first()
    if default_employee:
        return default_employee.pk
    return 1  # Fallback value; ensure that an Employee with pk=1 exists

class EmployeeRoleManangementModel(models.Model):
    employee = models.ForeignKey(
        EmployeeDetailsModel,
        on_delete=models.CASCADE,
        related_name="roles",
        default=get_default_employee_pk  # Provide default for existing rows
    )
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default="Default Role")
    permissions = models.JSONField(default=dict, help_text="Permissions for the role")

    def __str__(self):
        emp_name = self.employee.name if self.employee else "No Employee"
        return f"{emp_name} - {self.role}"
