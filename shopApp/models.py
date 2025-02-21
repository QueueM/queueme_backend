from django.db import models

# Create your models here.

from companyApp.models import CompanyDetailsModel
from django.contrib.auth.models import User
from shopServiceApp.models import ShopServiceCategoryModel

class ShopOpeningHoursModel(models.Model):
    class DAYS_OF_WEEK(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', "Wednesday"
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    shop = models.ForeignKey('ShopDetailsModel', related_name="opening_hours", on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK.choices)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('shop', 'day')
    
    def __str__(self):
        return f"{self.shop.name} - {self.day}: {self.open_time} to {self.close_time}" if not self.is_closed else f"{self.shop.name} - {self.day}: Closed"
class ShopDetailsModel(models.Model):
    class TARGET_CUSTOMER_CHOICES(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        BOTH = 'both', "Both"

    class SERVICES_TYPES_CHOICES(models.TextChoices):
        IN_SHOP = 'in_shop', 'In Shop'
        AT_HOME = 'at_home', 'At Home'
        BOTH = 'both', "Both"
        
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyDetailsModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='images/shop/cover', null=True)
    avatar_image = models.ImageField(upload_to='images/shopgallery/', null=True, blank=True)

    #
    username = models.CharField(max_length=20, default="", blank=True, unique=True)
    shop_name = models.CharField(max_length=300, default="")
    country = models.CharField(max_length=80, default="", blank=True)
    city = models.CharField(max_length=300, default="", blank=True)
    district = models.CharField(max_length=300, default="", blank=True)
    customers_type = models.CharField(choices=TARGET_CUSTOMER_CHOICES.choices, max_length=300, default=TARGET_CUSTOMER_CHOICES.BOTH)
    services_types = models.CharField(choices=SERVICES_TYPES_CHOICES.choices, max_length=300, default=SERVICES_TYPES_CHOICES.IN_SHOP)
    categories = models.ManyToManyField(ShopServiceCategoryModel, related_name="shops", blank=True, null=True)  # Many-to-Many relationship




# class ShopEmployeeDetailsModel(models.Model):
#     shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)
#     name = models.CharField(max_length=300)


class ShopPermissionsModel(models.Model):
    company = models.ForeignKey(CompanyDetailsModel, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)

    # Specific Permissions
    can_create_product = models.BooleanField(default=False)
    can_view_product = models.BooleanField(default=True)
    can_edit_product = models.BooleanField(default=False)
    can_delete_product = models.BooleanField(default=False)

class ShopGalleryImagesModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/shopgallery')

class SpecialistTypesModel(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return f"({self.id}){self.name}"

class ShopSpecialistDetailsModel(models.Model):
    # GENDER_CHOICES = [
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    # ]
    class SERVICE_LOCATION_CHOICES(models.TextChoices):
        IN_STORE = 'in_store', 'In Store'
        AT_SHOP = 'at_shop', 'At Shop'
        BOTH = 'both', "Both"
    employee = models.OneToOneField("employeeApp.EmployeeDetailsModel", on_delete=models.CASCADE, related_name="specialist")
    # name = models.CharField(max_length=300)
    speciality = models.CharField(max_length=300)
    shop = models.ManyToManyField(ShopDetailsModel)
    # phone_number = models.CharField(max_length=20)
    # gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    service_locatioin = models.CharField( max_length=20, choices=SERVICE_LOCATION_CHOICES.choices, default=SERVICE_LOCATION_CHOICES.BOTH)
    specialist_type = models.ManyToManyField(SpecialistTypesModel)
    services = models.ManyToManyField("shopServiceApp.ShopServiceDetailsModel")
    is_active = models.BooleanField(default=True)
    avatar_image = models.ImageField(upload_to='specialist/avatar_image/', null=True, blank=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"({self.id}){self.employee.name}"



