from django.contrib import admin
from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceGalleryModel,
    ShopServiceTimeSlotModel
)

class ShopServiceTimeSlotInline(admin.TabularInline):
    model = ShopServiceTimeSlotModel
    extra = 1

@admin.register(ShopServiceCategoryModel)
class ShopServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    readonly_fields = ('forecast_data',)
    ordering = ('-created_at',)

@admin.register(ShopServiceDetailsModel)
class ShopServiceDetailsAdmin(admin.ModelAdmin):
    inlines = [ShopServiceTimeSlotInline]
    list_display = ('name', 'shop', 'price', 'duration', 'created_at')
    readonly_fields = ('forecast_data',)
    ordering = ('-created_at',)

@admin.register(ServiceBookingDetailsModel)
class ServiceBookingDetailsAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer', 'booking_date', 'booking_time', 'status', 'fraud_flag', 'created_at')
    list_filter = ('status', 'fraud_flag', 'created_at')
    readonly_fields = ('fraud_flag',)
    ordering = ('-created_at',)

@admin.register(ServiceBookingDiscountCouponsModel)
class ServiceBookingDiscountCouponsAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'apply_to_all_services')
    search_fields = ('code',)

@admin.register(ShopServiceGalleryModel)
class ShopServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'service')
