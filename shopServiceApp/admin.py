# shopServiceApp/admin.py
from django.contrib import admin
from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceExtendedDetailsModel,
    ServiceOverview,
    ServiceFAQ,
    ServiceProcessStep,
    ServiceBenefit,
    ServiceAftercareTip,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceGalleryModel,
    ShopServiceTimeSlotModel,
)

class ShopServiceTimeSlotInline(admin.TabularInline):
    model = ShopServiceTimeSlotModel
    extra = 1

class ServiceOverviewInline(admin.TabularInline):
    model = ServiceOverview
    extra = 1

class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1

class ServiceProcessStepInline(admin.TabularInline):
    model = ServiceProcessStep
    extra = 1

class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1

class ServiceAftercareTipInline(admin.TabularInline):
    model = ServiceAftercareTip
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

@admin.register(ServiceExtendedDetailsModel)
class ServiceExtendedDetailsAdmin(admin.ModelAdmin):
    inlines = [
        ServiceOverviewInline,
        ServiceFAQInline,
        ServiceProcessStepInline,
        ServiceBenefitInline,
        ServiceAftercareTipInline,
    ]
    list_display = ('id', 'service', 'updated_at')
    search_fields = ('service__name',)

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
