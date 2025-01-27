from django.db import models

# Create your models here.

from django.contrib.auth.models import User
class CustomersDetailsModel(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    GENTER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        # ("others", "Others")
    ]
    name = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthDate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENTER_CHOICES, blank=True, null=True)