from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from shopServiceApp.models import ShopServiceCategoryModel
class CustomersDetailsModel(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")
    GENTER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        # ("others", "Others")
    ]
    class CUSTOMER_TYPE_CHOICES(models.TextChoices):
        REGULAR = 'regular', 'Regular'
        VIP = 'vip', 'VIP'
        NEW_CUSTOMER = 'new_customer', 'New Customer'
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENTER_CHOICES, blank=True, null=True)
    profie_photo = models.ImageField(upload_to='images/customerprofile', null=True, blank=True)
    preferred_services = models.ManyToManyField(ShopServiceCategoryModel, related_name="services", null=True, blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default=CUSTOMER_TYPE_CHOICES.NEW_CUSTOMER)
    address = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return f"({self.id}) {self.name}"
