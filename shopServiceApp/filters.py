

from django_filters import rest_framework as filters
from .models import ShopServiceGalleryModel

class ShopServiceGalleryFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopServiceGalleryModel
        fields = ['service']