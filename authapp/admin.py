from django.contrib import admin

# Register your models here.

from .models import SendOTPModel

admin.site.register(SendOTPModel)