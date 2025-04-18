# File: usersapp/models.py
from django.db import models
from django.contrib.auth.models import User
from helpers.phone_utils import normalize_phone_number

class UserProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(max_length=20, default="user")
    user_image = models.ImageField(upload_to='images/userprofile', blank=True, null=True)
    card_token = models.CharField(max_length=255, blank=True, null=True)  # For recurring billing

    def save(self, *args, **kwargs):
        if self.phone_number:
            try:
                # Always normalize the phone number before saving
                self.phone_number = normalize_phone_number(self.phone_number)
            except Exception:
                # In case normalization fails, you could also raise an error instead.
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
