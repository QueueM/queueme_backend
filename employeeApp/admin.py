from django.contrib import admin

# Register your models here.
from .models import EmployeeDetailsModel, EmployeeRoleManangementModel, EmployeeWorkingHoursModel

class EmployeeWorkingHoursInline(admin.TabularInline):
    model = EmployeeWorkingHoursModel
    extra = 1

class EmployeeDetailsAdmin(admin.ModelAdmin):
    inlines = [EmployeeWorkingHoursInline]

admin.site.register(EmployeeDetailsModel, EmployeeDetailsAdmin)
admin.site.register(EmployeeRoleManangementModel)

