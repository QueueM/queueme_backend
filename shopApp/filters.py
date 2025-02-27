from django_filters import rest_framework as filters
from .models import ShopGalleryImagesModel
from .models import ShopDetailsModel
from .models import ShopSpecialistDetailsModel
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.db.models import Q
from customClasses.BaseFilterSet import BaseFilterSet
class ShopGalleryImagesFilter(BaseFilterSet):
    # group = filters.NumberFilter(field_name='group')

    class Meta:
        model = ShopGalleryImagesModel
        # fields = ['shop']
        # fields = '__all__'
        exclude = ['image']

class ShopDetailsViewsetFilter(BaseFilterSet):
    # group = filters.NumberFilter(field_name='group')
    query = CharFilter(method='filter_query')
    class Meta:
        model = ShopDetailsModel
        # fields = ['company']
        # fields = '__all__'
        exclude = ['cover_image','avatar_image']
    
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            # name__icontains=value
            # Q(name__icontains=value) | Q(id__icontains=value)
            Q(name__icontains=value) | Q(id__icontains=value)
        )

class ShopSpecialistDetailsFilter(BaseFilterSet):
    query = CharFilter(method='filter_query')
    # shop = filters.ModelMultipleChoiceFilter(
    #     queryset=ShopDetailsModel.objects.all(),
    #     field_name="shop",
    #     to_field_name="id"
    # )
    class Meta:
        model = ShopSpecialistDetailsModel
        # fields = ["shop", "shop__company"]
        # fields = '__all__'
        exclude = 'avatar_image'
    
    def filter_query(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(id__icontains=value)
        )