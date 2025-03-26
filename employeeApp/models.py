from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ValidationError
from shopApp.models import ShopDetailsModel

class EmployeeWorkingHoursModel(models.Model):
    class DAYS_OF_WEEK(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', "Wednesday"
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    employee = models.ForeignKey('employeeApp.EmployeeDetailsModel', related_name="working_hours", on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'day')
    
    def __str__(self):
        return f"{self.employee.name} - {self.day}: {self.start_time} to {self.end_time}" if not self.is_closed else f"{self.employee.name} - {self.day}: Not working"

class EmployeeDetailsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee")
    shop = models.ForeignKey("shopApp.ShopDetailsModel", on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200, unique=True)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    avatar_image = models.ImageField(upload_to='employee/avatar_image/', null=True, blank=True)
    is_active = models.BooleanField()

    employee_id = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        users = User.objects.filter(username=self.phone_number)
        if users.exists():
            user = User.objects.get(username=self.phone_number)
            self.user = user
        else :
            user = User(username=self.phone_number)
            user.save()
            self.user = user 
        if not self.employee_id:
            last_employee = EmployeeDetailsModel.objects.filter(shop=self.shop).order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id.split('-')[-1])
                self.employee_id = f"{self.shop.username}-{last_id + 1}"
            else:
                self.employee_id = f"{self.shop.username}-1"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"({self.id}) {self.name}"

class EmployeeRoleManangementModel(models.Model):
    name = models.CharField(max_length=300)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE, related_name="role")
    employees = models.ManyToManyField(EmployeeDetailsModel, related_name="roles")

    # Shop Permissions
    can_view_shops = models.BooleanField(default=True)
    can_add_shops = models.BooleanField(default=True)
    can_edit_shops = models.BooleanField(default=True)
    can_delete_shops = models.BooleanField(default=False)

    # Customer Permissions
    can_view_customers = models.BooleanField(default=True)
    can_add_customers = models.BooleanField(default=True)
    can_edit_customers = models.BooleanField(default=True)

    # Service Permissions
    can_view_services = models.BooleanField(default=True)
    can_add_services = models.BooleanField(default=True)
    can_edit_services = models.BooleanField(default=True)
    can_delete_services = models.BooleanField(default=False)

    # Booking Permissions
    can_view_bookings = models.BooleanField(default=True)
    can_add_bookings = models.BooleanField(default=True)
    can_edit_bookings = models.BooleanField(default=True)
    can_delete_bookings = models.BooleanField(default=False)

    # Employee Permissions
    can_view_employees = models.BooleanField(default=True)
    can_add_employees = models.BooleanField(default=True)
    can_edit_employees = models.BooleanField(default=True)
    can_delete_employees = models.BooleanField(default=False)

    # Role Permissions
    can_view_roles = models.BooleanField(default=True)
    can_add_roles = models.BooleanField(default=True)
    can_edit_roles = models.BooleanField(default=True)
    can_delete_roles = models.BooleanField(default=False)

    # Specialist Permissions
    can_view_specialists = models.BooleanField(default=True)
    can_add_specialists = models.BooleanField(default=True)
    can_edit_specialists = models.BooleanField(default=True)
    can_delete_specialists = models.BooleanField(default=False)

    # Reels Permissions
    can_view_reels = models.BooleanField(default=True)
    can_add_reels = models.BooleanField(default=True)
    can_edit_reels = models.BooleanField(default=True)
    can_delete_reels = models.BooleanField(default=False)

    # Stories Permissions
    can_view_stories = models.BooleanField(default=True)
    can_add_stories = models.BooleanField(default=True)
    can_edit_stories = models.BooleanField(default=True)
    can_delete_stories = models.BooleanField(default=False)

    # Marketing Ads Permissions
    can_view_marketing_ads = models.BooleanField(default=True)
    can_add_marketing_ads = models.BooleanField(default=True)
    can_edit_marketing_ads = models.BooleanField(default=True)
    can_delete_marketing_ads = models.BooleanField(default=False)

    # Chat Permissions
    can_view_chat = models.BooleanField(default=True)
    can_add_chat = models.BooleanField(default=True)
    can_edit_chat = models.BooleanField(default=True)
    can_delete_chat = models.BooleanField(default=False)


    # class Meta:
    #     unique_together = ('shop', 'employee')

    def clean(self):
        """
        Ensures that an employee has only one role per shop.
        """
        for employee in self.employees.all():
            existing_roles = EmployeeRoleManangementModel.objects.filter(shop=self.shop, employees=employee).exclude(id=self.id)
            if existing_roles.exists():
                raise ValidationError(f"Employee {employee.name} already has a role in shop {self.shop.name}.")

    def __str__(self):
        return f"{self.shop} - {self.name}"