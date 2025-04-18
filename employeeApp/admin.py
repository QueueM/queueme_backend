from django.contrib import admin
from .models import EmployeeDetailsModel, EmployeeWorkingHoursModel, EmployeeRoleManangementModel

@admin.register(EmployeeDetailsModel)
class EmployeeDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'shop', 'position', 'ai_performance_data')
    search_fields = ('name', 'shop__shop_name', 'company__name')

@admin.register(EmployeeWorkingHoursModel)
class EmployeeWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'day', 'start_time', 'end_time')

@admin.register(EmployeeRoleManangementModel)
class EmployeeRoleManagementAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'role', 'shop')
