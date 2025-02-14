from django.contrib import admin

# Register your models here.

from .models import ShopServiceDetailsModel, ServiceBookingDiscountCouponsModel
from .models import ShopServiceCategoryModel, ServiceBookingDetailsModel
from .models import ShopServiceTimeSlotModel

class ShopServiceTimeSlotInline(admin.TabularInline):
    model = ShopServiceTimeSlotModel
    extra = 1

class ShopServiceDetailsAdmin(admin.ModelAdmin):
    inlines = [ShopServiceTimeSlotInline]

admin.site.register(ShopServiceDetailsModel, ShopServiceDetailsAdmin)
admin.site.register(ShopServiceCategoryModel)
admin.site.register(ServiceBookingDiscountCouponsModel)
admin.site.register(ServiceBookingDetailsModel)