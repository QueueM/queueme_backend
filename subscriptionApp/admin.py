from django.contrib import admin

# Register your models here.

from .models import (UserSubscriptionPlansModels, UserSubscriptionDetailsModel,
                     CompanySubscriptionDetailsModel, CompanySubscriptionPlansModel,
                     Payment)


admin.site.register(CompanySubscriptionDetailsModel)
admin.site.register(CompanySubscriptionPlansModel)
admin.site.register(Payment)
