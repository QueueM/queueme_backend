from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfileModel(models.Model):
    # first_name = models.CharField(max_length=120)
    # last_name = models.CharField(max_length=120)
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('company', 'Company'),
        ('company_manager', 'Company Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20, default="user")
    user_image = models.ImageField(upload_to='images/userprofile')
    
