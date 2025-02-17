from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    shop = models.ForeignKey("shopApp.ShopDetailsModel", on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    avatar_image = models.ImageField(upload_to='employee/avatar_image/', null=True, blank=True)
    is_active = models.BooleanField()

    employee_id = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = EmployeeDetailsModel.objects.filter(shop=self.shop).order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id.split('-')[-1])
                self.employee_id = f"{self.shop.username}-{last_id + 1}"
            else:
                self.employee_id = f"{self.shop.username}-1"
        super().save(*args, **kwargs)

