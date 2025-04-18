from django.contrib import admin
from .models import CompanyDetailsModel

@admin.register(CompanyDetailsModel)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'is_verified', 'status', 'shops_limit', 'merchant_type', 'online_payment_global_enabled', 'fraud_flag', 'created_at')
    readonly_fields = ('forecast_data', 'fraud_flag', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('status', 'merchant_type', 'fraud_flag', 'online_payment_global_enabled')
