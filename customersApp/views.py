from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .serializers import CustomersDetailsModelSerializer
from .models import CustomersDetailsModel

class CustomersDetailsModelViewSet(viewsets.ModelViewSet):
    queryset = CustomersDetailsModel.objects.all()
    serializer_class = CustomersDetailsModelSerializer