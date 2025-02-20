from django.shortcuts import render

# Create your views here.



from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import EmployeeDetailsModel
from .serializers import EmployeeDetailsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import EmployeeDetailsFilter

class EmployeeDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeDetailsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeDetailsFilter