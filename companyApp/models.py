from django.db import models
from django.contrib.auth.models import User
# from shopApp.models import ShopDetailsModel
from django.apps import apps

# Create your models here.


class CompanyDetailsModel(models.Model):
    STATUS_CHOICES = [
        ("accepted",  "Accepted"),
        ("Rejected",  "Rejected"),
        ("created",  "created")
    ]
    class DAYS_MERCHANT_TYPE(models.TextChoices):
        FREELANCE = 'freelance', 'Freelance'
        SHOP = 'shop', 'Shop'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=300)
    company_image = models.ImageField(upload_to='images/companylogo', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, default="created")
    shops_limit = models.IntegerField(default=1)
    merchant_type = models.CharField(max_length=20, choices=DAYS_MERCHANT_TYPE.choices, default=DAYS_MERCHANT_TYPE.FREELANCE)
    name_arabic = models.CharField(max_length=300, default="")
    company_registration_document = models.FileField(upload_to='company_registration_doc/', null=True, blank=True)
    tax_registration_number = models.CharField(max_length=30, default="")
    
    def __str__(self):
        return self.name


# class CompanyEmployeeDetailsModel(models.Model):
#     shop = models.ForeignKey("shopApp.ShopDetailsModel", on_delete = models.CASCADE)
#     # company = models.ForeignKey(CompanyDetailsModel, on_delete = models.CASCADE)
#     name = models.CharField(max_length=300)
#     designation = models.CharField(max_length=50, null=True, blank=True)
#     phone_number = models.CharField(max_length=30, null=True, blank=True)
#     salary = models.FloatField(null=True, blank=True)


# class CompanyEmployeeRoleManagementModel(models.Model):
#     employee = models.ForeignKey(CompanyEmployeeDetailsModel, on_delete=models.CASCADE)
#     shop = models.ForeignKey("shopApp.ShopDetailsModel", on_delete=models.CASCADE)
#     can_create_product = models.BooleanField(default=False)
#     can_edit_product = models.BooleanField(default=False)
#     can_list_product = models.BooleanField(default=False)
    


