from django_filters import rest_framework as filters
from .models import ShopGalleryImagesModel

class ShopGalleryImagesFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopGalleryImagesModel
        fields = ['shop']