# File: customersApp/models.py

from django.db import models
from django.contrib.auth.models import User
from shopServiceApp.models import ShopServiceCategoryModel

# ──────────────────────────────────────────────────────────────────────────────
# Move TextChoices out into their own top‐level class
# ──────────────────────────────────────────────────────────────────────────────
class CustomerTypeEnum(models.TextChoices):
    REGULAR      = 'regular',      'Regular'
    VIP          = 'vip',          'VIP'
    NEW_CUSTOMER = 'new_customer', 'New Customer'


class CustomersDetailsModel(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="customer"
    )

    GENDER_CHOICES = [
        ("male",   "Male"),
        ("female", "Female"),
    ]

    name           = models.CharField(max_length=300)
    phone_number   = models.CharField(max_length=20, blank=True, null=True)
    birth_date     = models.DateField(null=True, blank=True)
    gender         = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True, null=True)
    profile_photo  = models.ImageField(upload_to='images/customerprofile', null=True, blank=True)

    preferred_services = models.ManyToManyField(
        ShopServiceCategoryModel,
        related_name="preferred_by_customers",
        blank=True
    )

    customer_type = models.CharField(
        max_length=20,
        choices=CustomerTypeEnum.choices,
        default=CustomerTypeEnum.NEW_CUSTOMER
    )

    address = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return f"({self.id}) {self.name}"
