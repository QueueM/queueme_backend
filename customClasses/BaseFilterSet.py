from django_filters import rest_framework as filters
from django.db.models import ForeignKey, ManyToManyField, ImageField, FileField
from functools import partial

class BaseFilterSet(filters.FilterSet):
    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        if isinstance(f, (ImageField, FileField)):
            return None
        return super().filter_for_field(f, name, lookup_expr)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self.Meta.model
        for field in model._meta.get_fields():
            if isinstance(field, (ForeignKey, ManyToManyField)):
                field_name = field.name
                self.filters[field_name] = filters.CharFilter(
                    method=partial(self.filter_multiple_values, field_name)
                )

    def filter_multiple_values(self, field_name, queryset, name, value):
        values = value.split(",")
        return queryset.filter(**{f"{field_name}__in": values})
