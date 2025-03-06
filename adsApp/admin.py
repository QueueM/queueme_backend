from django.contrib import admin

# Register your models here.

from .models import ShopAdsImpressionModel, ShopAdsModel

admin.site.register(ShopAdsImpressionModel)
admin.site.register(ShopAdsModel)