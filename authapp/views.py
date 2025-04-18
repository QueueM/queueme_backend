# File: authapp/views.py

import logging
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_spectacular.utils import extend_schema
from django.conf import settings
from .serializers import (
    RegistrationOTPRequestSerializer,
    RegistrationOTPResponseSerializer,
    TestResponseSerializer,
    RegisterUserRequestSerializer,
    RegisterUserResponseSerializer,
    LoginWithOTPRequestSerializer,
    LoginWithOTPResponseSerializer,
    UnifiedLoginRequestSerializer,
    UnifiedLoginResponseSerializer,
)
from .models import SendOTPModel
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from usersapp.serializers import UserSerializer
from companyApp.serializers import CompanyDetailsModelSerializer
from customersApp.serializers import CustomersDetailsModelSerializer
from employeeApp.serializers import EmployeeDetailsSerializer
from helpers.phone_utils import normalize_phone_number

logger = logging.getLogger(__name__)

@extend_schema(
    request=RegistrationOTPRequestSerializer,
    responses=RegistrationOTPResponseSerializer,
)
class RegistrationOTPAPIView(GenericAPIView):
    """
    GET /get-otp/?phone_number=...&otp_type=...
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationOTPRequestSerializer

    def get(self, request, *args, **kwargs):
        data = RegistrationOTPRequestSerializer(data=request.GET)
        data.is_valid(raise_exception=True)
        phone = normalize_phone_number(data.validated_data['phone_number'])
        otp_type = data.validated_data['otp_type']
        # ... your OTP logic here ...
        otp = "2222"  # dev only
        SendOTPModel.objects.filter(phone_number=phone).delete()
        record = SendOTPModel.objects.create(
            phone_number=phone, otp=otp, otp_type=otp_type, otp_mode='phone'
        )
        logger.info("OTP sent to %s", phone)
        resp = {'message': 'OTP sent successfully'}
        if settings.DEBUG:
            resp['otp'] = otp
        return Response(resp, status=status.HTTP_200_OK)


@extend_schema(responses=TestResponseSerializer)
class TestAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TestResponseSerializer

    def get(self, request, *args, **kwargs):
        return Response({'name': 'Aman Ansari'})


@extend_schema(
    request=RegisterUserRequestSerializer,
    responses=RegisterUserResponseSerializer,
)
class RegisterAPIView(GenericAPIView):
    """
    POST /register/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = normalize_phone_number(serializer.validated_data['phone_number'])
        otp = serializer.validated_data['otp']
        # ... validate OTP ...
        password = serializer.validated_data['password']
        if User.objects.filter(username=phone).exists():
            return Response(
                {"message": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.create_user(username=phone, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully!",
            "user_id": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    request=LoginWithOTPRequestSerializer,
    responses=LoginWithOTPResponseSerializer,
)
class LoginWithOTPAPIView(GenericAPIView):
    """
    POST /get-token-with-otp/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginWithOTPRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = normalize_phone_number(serializer.validated_data['phone_number'])
        otp = serializer.validated_data['otp']
        # ... validate OTP ...
        user = User.objects.get(username=phone)
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        customer = CustomersDetailsModelSerializer(
            CustomersDetailsModel.objects.filter(user=user).first()
        ).data if CustomersDetailsModel.objects.filter(user=user).exists() else None
        company = CompanyDetailsModelSerializer(
            CompanyDetailsModel.objects.filter(user=user).first()
        ).data if CompanyDetailsModel.objects.filter(user=user).exists() else None
        employee = EmployeeDetailsSerializer(
            EmployeeDetailsModel.objects.filter(user=user).first()
        ).data if EmployeeDetailsModel.objects.filter(user=user).exists() else None
        return Response({
            "user_details": user_data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "customer_details": customer,
            "company_details": company,
            "employee_details": employee,
        })


@extend_schema(
    request=UnifiedLoginRequestSerializer,
    responses=UnifiedLoginResponseSerializer,
)
class UnifiedLoginWithOTPAPIView(GenericAPIView):
    """
    POST /unified-login/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UnifiedLoginRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = normalize_phone_number(serializer.validated_data['phone_number'])
        otp = serializer.validated_data['otp']
        # ... validate OTP ...
        user = User.objects.get(username=phone)
        # determine roles
        roles = []
        if hasattr(user, 'company'):
            roles.append("company")
        if hasattr(user, 'employee'):
            roles.append("employee")
        if ShopDetailsModel.objects.filter(manager_phone_number=phone).exists():
            roles.append("manager")
        if not roles:
            roles.append("customer")
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "roles": roles,
        })
