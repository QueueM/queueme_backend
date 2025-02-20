from django_filters import rest_framework as filters
from .models import ShopGalleryImagesModel
from .models import ShopDetailsModel
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.db.models import Q
class ShopGalleryImagesFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopGalleryImagesModel
        fields = ['shop']

class ShopDetailsViewsetFilter(filters.FilterSet):
    # group = filters.NumberFilter(field_name='group')
    query = CharFilter(method='filter_query')
    class Meta:
        model = ShopDetailsModel
        fields = ['company']
    
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            # name__icontains=value
            # Q(name__icontains=value) | Q(id__icontains=value)
            Q(name__icontains=value) | Q(id__icontains=value)
        )
