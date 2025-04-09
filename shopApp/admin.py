# shopApp/admin.py
from django.contrib import admin
from .models import (
    ShopDetailsModel, 
    ShopGalleryImagesModel, 
    ShopSpecialistDetailsModel, 
    SpecialistTypesModel
)

@admin.register(ShopDetailsModel)
class ShopDetailsAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'owner', 'company', 'created_at', 'ai_recommendations', 'ai_personalization')
    search_fields = ('shop_name', 'owner__username', 'company__name')
    list_filter = ('created_at',)
    readonly_fields = ('ai_recommendations', 'ai_personalization')

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
