from django.db import models

# Create your models here.

from companyApp.models import CompanyDetailsModel
from django.contrib.auth.models import User
from companyApp.models import CompanyEmployeeDetailsModel 
class ShopDetailsModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyDetailsModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    note = models.CharField(max_length=300, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

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

class ShopSpecialistDetailsModel(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    employee = models.OneToOneField(CompanyEmployeeDetailsModel, on_delete=models.CASCADE, related_name="specialist")
    name = models.CharField(max_length=300)
    speciality = models.CharField(max_length=300)
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    rating = models.FloatField(default=0.0)



