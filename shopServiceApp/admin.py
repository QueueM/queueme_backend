from django.contrib import admin

# Register your models here.

from .models import ShopServiceDetailsModel, ServiceBookingDiscountCouponsModel
from .models import ShopServiceCategoryModel, ServiceBookingDetailsModel

admin.site.register(ShopServiceDetailsModel)
admin.site.register(ShopServiceCategoryModel)
admin.site.register(ServiceBookingDiscountCouponsModel)
admin.site.register(ServiceBookingDetailsModel)