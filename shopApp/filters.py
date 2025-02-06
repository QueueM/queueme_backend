from django_filters import rest_framework as filters
from .models import ShopGalleryImagesModel
from .models import ShopDetailsModel
class ShopGalleryImagesFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopGalleryImagesModel
        fields = ['shop']

class ShopDetailsViewsetFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopDetailsModel
        fields = ['company']

