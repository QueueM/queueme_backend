# shopApp/admin.py
from django.contrib import admin
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    SpecialistTypesModel,
    ShopOpeningHoursModel,
)
from usersapp.models import UserProfileModel
from companyApp.models import CompanyDetailsModel  # For explicit checking

class ShopDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_name', 'owner', 'company', 'manager_phone_number', 'created_at')
    readonly_fields = ('ai_recommendations', 'ai_personalization', 'created_at')
    search_fields = ('shop_name', 'owner__username', 'company__name', 'manager_phone_number')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # First, allow superuser or company admin (if company exists) to see all shops for that company.
        if request.user.is_superuser:
            return qs
        try:
            # Check if the user has an associated company.
            company = request.user.company  # This will raise RelatedObjectDoesNotExist if none exists.
        except CompanyDetailsModel.DoesNotExist:
            company = None
        
        if company:
            # If user is a company admin (or similar) and has an associated company, filter by company.
            return qs.filter(company=company)
        
        # Otherwise, assume the user is a manager.
        try:
            profile = UserProfileModel.objects.get(user=request.user)
            return qs.filter(manager_phone_number=profile.phone_number)
        except UserProfileModel.DoesNotExist:
            return qs.none()

admin.site.register(ShopDetailsModel, ShopDetailsAdmin)

@admin.register(ShopGalleryImagesModel)
class ShopGalleryImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop')
    search_fields = ('shop__shop_name',)

@admin.register(ShopSpecialistDetailsModel)
class ShopSpecialistDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'speciality', 'get_shops', 'rating', 'is_active')
    search_fields = ('speciality',)
    
    def get_shops(self, obj):
        return ", ".join([shop.shop_name for shop in obj.shop.all()])
    get_shops.short_description = "Shops"

@admin.register(SpecialistTypesModel)
class SpecialistTypesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ShopOpeningHoursModel)
class ShopOpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'day', 'open_time', 'close_time', 'is_closed')
    list_filter = ('day', 'is_closed')
