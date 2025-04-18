# File: shopServiceApp/admin.py

from django.contrib import admin
from .models import (
    ShopServiceCategoryModel,
    ShopServiceTimeSlotModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel,
    ServiceBookingDiscountCouponsModel,
    ShopServiceGalleryModel,
    ServiceExtendedDetailsModel,
    ServiceOverview,
    ServiceFAQ,
    ServiceProcessStep,
    ServiceBenefit,
    ServiceAftercareTip,
)

@admin.register(ShopServiceCategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(ShopServiceTimeSlotModel)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('service', 'day', 'start_time', 'end_time')


@admin.register(ShopServiceDetailsModel)
class ServiceDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'service_type', 'price', 'is_available')


admin.site.register(ServiceBookingDetailsModel)
admin.site.register(ServiceBookingDiscountCouponsModel)
admin.site.register(ShopServiceGalleryModel)

# Extended-details in admin
admin.site.register(ServiceExtendedDetailsModel)
admin.site.register(ServiceOverview)
admin.site.register(ServiceFAQ)
admin.site.register(ServiceProcessStep)
admin.site.register(ServiceBenefit)
admin.site.register(ServiceAftercareTip)
