from django.contrib import admin

# Register your models here.
from .models import ShopDetailsModel, ShopGalleryImagesModel, ShopSpecialistDetailsModel, SpecialistTypesModel

admin.site.register(ShopDetailsModel)
admin.site.register(ShopGalleryImagesModel)
admin.site.register(ShopSpecialistDetailsModel)
admin.site.register(SpecialistTypesModel)