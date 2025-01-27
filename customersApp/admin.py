from django.contrib import admin

# Register your models here.

from .models import CustomersDetailsModel

admin.site.register(CustomersDetailsModel)