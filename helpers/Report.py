from django.apps import apps

class ModelReportGenerator:
    def __init__(self, model_name: str, app_label: str):
        self.model = apps.get_model(app_label=app_label, model_name=model_name)
        if not self.model:
            raise ValueError(f"Model {model_name} not found in app {app_label}")
        

    def generate(
        self,
        filters: dict = None,
        group_by: list = None,
        aggregations: dict = None,
        order_by: list = None,
    ):
   
      
        queryset = self.model.objects.all()

        if filters:
            queryset = queryset.filter(**filters)

        if group_by:
            queryset = queryset.values(*group_by)

        if aggregations:
            queryset = queryset.annotate(**aggregations)

        if order_by:
            queryset = queryset.order_by(*order_by)

        return queryset
