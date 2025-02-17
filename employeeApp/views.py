from django.shortcuts import render

# Create your views here.



from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import EmployeeDetailsModel
from .serializers import EmployeeDetailsSerializer


class EmployeeDetailsViewset(CustomBaseModelViewSet):
    queryset = EmployeeDetailsModel.objects.all()
    serializer_class = EmployeeDetailsSerializer