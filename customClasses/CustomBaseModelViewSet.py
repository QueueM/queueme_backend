from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from helpers.PaginationClass import CustomPageNumberPagination

class CustomBaseModelViewSet_ChoicesMixin:
    @action(detail=False, methods=['get'], url_path='choices', url_name='choices')
    def choices(self, request, *args, **kwargs):
        model = self.queryset.model
        choices = {}
        for field in model._meta.fields:
            if field.choices:
                choices[field.name + "_choices"] = [{'key': key, 'value': value} for key, value in field.choices]
        return Response(choices)
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        include_choices = request.query_params.get('get_model_choices', 'false').lower() == 'true'
        if include_choices:
            model = self.queryset.model
            choices = {}
            for field in model._meta.fields:
                if field.choices:
                    choices[field.name + "_choices"] = [{"key": key, "value": value} for key, value in field.choices]
            response.data.update(choices)
        return response

class CustomBaseModelViewSet(CustomBaseModelViewSet_ChoicesMixin, ModelViewSet):
    pagination_class = CustomPageNumberPagination
