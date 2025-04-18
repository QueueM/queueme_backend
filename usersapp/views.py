# File: usersapp/views.py

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User
from .models import UserProfileModel
from .serializers import (
    UserSerializer,
    UserProfileModelSerializer,
    UpdateProfileSuggestRequestSerializer,
    UpdateProfileSuggestResponseSerializer,
    RegisterUserRequestSerializer,
    RegisterUserResponseSerializer,
    UserMasterDetailsResponseSerializer,
)
from authapp.models import SendOTPModel
from helpers.phone_utils import normalize_phone_number
from customersApp.models import CustomersDetailsModel
from customersApp.serializers import CustomersDetailsModelSerializer
from companyApp.models import CompanyDetailsModel
from companyApp.serializers import CompanyDetailsModelSerializer
from subscriptionApp.models import CompanySubscriptionDetailsModel
from subscriptionApp.serializers import CompanySubscriptionDetailsModelSerializer
from employeeApp.models import EmployeeDetailsModel
from employeeApp.serializers import EmployeeDetailsSerializer

class UpdateProfileSuggestAPIView(GenericAPIView):
    permission_classes = []
    serializer_class = UpdateProfileSuggestRequestSerializer

    @extend_schema(
        request=UpdateProfileSuggestRequestSerializer,
        responses=UpdateProfileSuggestResponseSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Implement suggestion logic here
        return Response({'message': 'Refer Code is not valid'}, status=status.HTTP_406_NOT_ACCEPTABLE)

class RegisterUserAPIView(GenericAPIView):
    permission_classes = []
    serializer_class = RegisterUserRequestSerializer

    @extend_schema(
        request=RegisterUserRequestSerializer,
        responses=RegisterUserResponseSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Normalize and validate phone number
        phone_number = normalize_phone_number(data['phone_number'])
        if UserProfileModel.objects.filter(phone_number=phone_number).exists():
            return Response({'message': 'Account already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=phone_number).exists():
            return Response({'message': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        # Validate OTP
        otp_record = SendOTPModel.objects.filter(otp=data['otp'], phone_number=phone_number)
        if not otp_record.exists():
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        # Create user and profile
        user = User(username=phone_number)
        user.save()
        user_profile = UserProfileModel(user=user, name=data['name'], phone_number=phone_number)
        user_profile.save()
        otp_record.delete()
        response_data = {
            'id': user_profile.id,
            'username': user.username,
            'name': user_profile.name,
            'phone_number': user_profile.phone_number,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserMasterDetailsAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserMasterDetailsResponseSerializer

    @extend_schema(responses=UserMasterDetailsResponseSerializer)
    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = UserSerializer(user).data
        customer = CustomersDetailsModel.objects.filter(user=user).first()
        customer_data = CustomersDetailsModelSerializer(customer).data if customer else None
        company = CompanyDetailsModel.objects.filter(user=user).first()
        company_data = CompanyDetailsModelSerializer(company).data if company else None
        employee = EmployeeDetailsModel.objects.filter(user=user).first()
        employee_data = EmployeeDetailsSerializer(employee).data if employee else None
        subscription = None
        subscription_data = None
        if company:
            subscription = CompanySubscriptionDetailsModel.objects.filter(company=company).first()
            subscription_data = CompanySubscriptionDetailsModelSerializer(subscription).data if subscription else None
        response_data = {
            'user': user_data,
            'customer_details': customer_data,
            'company_details': company_data,
            'employee_details': employee_data,
            'subscription_details': subscription_data,
        }
        return Response(response_data)

