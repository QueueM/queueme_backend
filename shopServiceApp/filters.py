

from django_filters import rest_framework as filters
from .models import ShopServiceGalleryModel, ServiceBookingDetailsModel, ShopServiceDetailsModel

class ShopServiceGalleryFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopServiceGalleryModel
        fields = ['service']


class ServiceBookingDetailsFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ServiceBookingDetailsModel
        fields = ['customer__user']

class ShopServiceDetailsFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopServiceDetailsModel
        fields = ['shop']