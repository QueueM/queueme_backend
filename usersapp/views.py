from django.shortcuts import render
# Create your views here.

from django.contrib.auth.models import User
from .models import UserProfileModel

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authapp.models import SendOTPModel

from .models import UserProfileModel
from .serializers import UserProfileModelSerializer
from helpers.PaginationClass import CustomPageNumberPagination
class Helper:
    def checkForKeys(keyList, requestBody):
        for a in keyList:
            if a not in requestBody:
                return {"message": "'referCode' field is required"}
            
        return False

class UpdateProfileSuggest(APIView):
    permission_classes = []
    def post(self, request):
        # Parse the request body (DRF automatically parses JSON into `request.data`)
        required_keys = ['username','password']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.data]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Additional processing can go here
        return Response({"errorMsg": "Refer Code is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class RegisterSellerAPIView(APIView):
    permission_classes = []
    def post(self, request):
        # Parse the request body (DRF automatically parses JSON into `request.data`)
        required_keys = ['name','phone_number', 'otp']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.data]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        name = request.data['name']
        phone_number = request['phone_number']
        otp = request['otp']

        return Response({"errorMsg": "Refer Code is not valid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class RegisterUserAPIView(APIView):
    permission_classes = []
    def post(self, request):
        # Parse the request body (DRF automatically parses JSON into `request.data`)
        required_keys = ['name','phone_number', 'otp']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.data]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # getting data
        name = request.data['name']
        phone_number = request.data['phone_number']
        otp = request.data['otp']

        #check phone number
        userProfile = UserProfileModel.objects.filter(phone_number=phone_number)
        if userProfile.exists():
            return Response({"message" : "Account with this phone number already exist"})
        # checking username
        user = User.objects.filter(username=phone_number)
        if user.exists():
            return Response({"message" : "Username already taken"})
        
        # Check otp validation
        otpRecord = SendOTPModel.objects.filter(otp=otp, phone_number=phone_number)
        if not otpRecord.exists():
            return Response({"message" : "Invalid OTP !!"})
        
        # create user
        user = User(username=phone_number)
        user.save()

        userProfile = UserProfileModel(user=user, name=name, phone_number=phone_number)
        userProfile.save()
        serializer = UserProfileModelSerializer(userProfile)

        # Delete otp
        otpRecord.delete()
        return Response(serializer.data)
    
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileModelSerializer
    pagination_class = CustomPageNumberPagination


from customersApp.models import CustomersDetailsModel
from customersApp.serializers import CustomersDetailsModelSerializer
from companyApp.models import CompanyDetailsModel
from companyApp.serializers import CompanyDetailsModelSerializer
from employeeApp.models import EmployeeDetailsModel
from employeeApp.serializers import EmployeeDetailsSerializer
class UserMasterDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get customer details if they exist
        customer = CustomersDetailsModel.objects.filter(user=user).first()
        customer_data = CustomersDetailsModelSerializer(customer).data if customer else None

        # Get company details if they exist
        company = CompanyDetailsModel.objects.filter(user=user).first()
        company_data = CompanyDetailsModelSerializer(company).data if company else None

        # Get employee details if they exist
        employee = EmployeeDetailsModel.objects.filter(user=user).first()
        employee_data = EmployeeDetailsSerializer(employee).data if employee else None

        return Response({
            "customer_details": customer_data,
            "company_details": company_data,
            "employee_details": employee_data
        })