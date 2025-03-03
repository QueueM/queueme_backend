from django.contrib import admin

# Register your models here.

from .models import UserSubscriptionPlansModels, UserSubscriptionDetailsModel
from .models import CompanySubscriptionDetailsModel, CompanySubscriptionPlansModel


admin.site.register(CompanySubscriptionDetailsModel)
admin.site.register(CompanySubscriptionPlansModel)