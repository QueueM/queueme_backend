from django.contrib import admin

# Register your models here.
from .models import CompanyDetailsModel, CompanyEmployeeDetailsModel, CompanyEmployeeRoleManagementModel


admin.site.register(CompanyDetailsModel)
admin.site.register(CompanyEmployeeDetailsModel)
admin.site.register(CompanyEmployeeRoleManagementModel)