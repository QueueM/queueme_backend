from django.contrib import admin

# Register your models here.

from .models import UserProfileModel

admin.site.register(UserProfileModel)