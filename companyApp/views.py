# File: companyApp/views.py

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterCompanyRequestSerializer,
    RegisterCompanyResponseSerializer,
)
from .models import CompanyDetailsModel
from django.contrib.auth.models import User

@extend_schema(
    request=RegisterCompanyRequestSerializer,
    responses=RegisterCompanyResponseSerializer,
)
class RegisterAsCompanyAPIView(GenericAPIView):
    """
    POST /company/register/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterCompanyRequestSerializer

    def post(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        data.is_valid(raise_exception=True)

        # Decode validated data
        user_id       = data.validated_data['user_id']
        company_name  = data.validated_data['company_name']
        address       = data.validated_data['address']
        phone_number  = data.validated_data['phone_number']

        # Business logic: create CompanyDetailsModel
        user = User.objects.get(pk=user_id)
        company = CompanyDetailsModel.objects.create(
            user=user,
            company_name=company_name,
            address=address,
            phone_number=phone_number,
        )

        # Prepare response
        resp = {
            'company': {
                'id': company.id,
                'company_name': company.company_name,
                'address': company.address,
                'phone_number': company.phone_number,
                # add any other fields you need
            }
        }
        return Response(resp, status=status.HTTP_201_CREATED)
