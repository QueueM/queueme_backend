from rest_framework import viewsets, filters
from .serializers import CustomersDetailsModelSerializer
from .models import CustomersDetailsModel
from .filters import CustomerDetailsViewsetFilter
from django_filters.rest_framework import DjangoFilterBackend
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet

class CustomersDetailsModelViewSet(viewsets.ModelViewSet):
    queryset = CustomersDetailsModel.objects.all()
    serializer_class = CustomersDetailsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = CustomerDetailsViewsetFilter
