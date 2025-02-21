from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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


class EmployeeRoleManangementModel(models.Model):
    name = models.CharField(max_length=300)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE, related_name="role")
    employee = models.ForeignKey(EmployeeDetailsModel, on_delete=models.CASCADE, related_name="role")
    can_edit_shop = models.BooleanField(default=False)
    can_add_services = models.BooleanField(default=False)
    can_edit_services = models.BooleanField(default=False)
    can_add_employee = models.BooleanField(default=False)
    can_edit_employee = models.BooleanField(default=False)
    can_delete_employee = models.BooleanField(default=False)
    can_add_specialist = models.BooleanField(default=False)
    can_edit_specialist = models.BooleanField(default=False)
    can_delete_specialist = models.BooleanField(default=False)

    class Meta:
        unique_together = ('shop', 'employee')

    def __str__(self):
        return f"{self.employee} - {self.shop} - {self.name}"