from django.contrib import admin

# Register your models here.

from .models import UserSubscriptionPlansModels, UserSubscriptionDetailsModel

admin.site.register(UserSubscriptionPlansModels)
admin.site.register(UserSubscriptionDetailsModel)