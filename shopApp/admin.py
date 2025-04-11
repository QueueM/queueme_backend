# shopApp/admin.py
from django.contrib import admin
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    SpecialistTypesModel,
    ShopOpeningHoursModel,
)

@admin.register(ShopDetailsModel)
class ShopDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'owner', 'company', 'online_payment_requested', 'online_payment_status', 'created_at')
    search_fields = ('shop_name', 'owner__username', 'company__name')
    list_filter = ('created_at', 'online_payment_requested', 'online_payment_status')
    readonly_fields = ('ai_recommendations', 'ai_personalization', 'created_at')

@admin.register(ShopGalleryImagesModel)
class ShopGalleryImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop')
    search_fields = ('shop__shop_name',)

@admin.register(ShopSpecialistDetailsModel)
class ShopSpecialistDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'speciality', 'shops_display', 'rating', 'is_active')
    search_fields = ('speciality', 'employee__name')

    def shops_display(self, obj):
        return ", ".join([shop.shop_name for shop in obj.shop.all()])
    shops_display.short_description = "Shops"

@admin.register(SpecialistTypesModel)
class SpecialistTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ShopOpeningHoursModel)
class ShopOpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'day', 'open_time', 'close_time', 'is_closed')
    list_filter = ('day', 'is_closed')
