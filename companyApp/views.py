from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User
from usersapp.models import UserProfileModel

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authapp.models import SendOTPModel

from .serializers import CompanyDetailsModelSerializer, CompanyEmployeeRoleManagementModelSerializer, CompanyEmployeeDetailsModelSerializer
from .models import CompanyDetailsModel, CompanyEmployeeRoleManagementModel, CompanyEmployeeDetailsModel
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
class RegisterAsCompanyAPIView(APIView):
    permission_classes = []
    def post(self, request):
        # Parse the request body (DRF automatically parses JSON into `request.data`)
        required_keys = ['username','company_name','name','phone_number', 'password', 'otp']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.data]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # getting data
        username = request.data['username']
        companyName = request.data['company_name']
        name = request.data['name']
        phone_number = request.data['phone_number']
        password = request.data['password']
        otp = request.data['otp']

        # check if user exist
        user = User.objects.filter(username=username)
        if user.exists():
            return Response({"message" : "User with same username already exist"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        # Check otp validation
        otpRecord = SendOTPModel.objects.filter(otp=otp, phone_number=phone_number)
        if not otpRecord.exists():
            return Response({"message" : "Invalid OTP !!"},status=status.HTTP_400_BAD_REQUEST)
        
        # create user
        user = User(username=username)
        user.set_password(password)
        user.save()

        userProfile = UserProfileModel(user=user, name=name, phone_number=phone_number)
        userProfile.save()

        companyDetails = CompanyDetailsModel(user=user, name=companyName)
        companyDetails.save()
        

        # Delete otp
        otpRecord.delete()
        serializer = CompanyDetailsModelSerializer(companyDetails)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class CompanyDetailsViewSet(viewsets.ModelViewSet):
    queryset = CompanyDetailsModel.objects.all()
    serializer_class = CompanyDetailsModelSerializer
    def get_queryset(self):
        """
        This view should return the company details associated with the current user.
        """
        return CompanyDetailsModel.objects.filter(user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user  # Pass the user into the context
        return context

class CompanyEmployeeDetailsModelViewSet(CustomBaseModelViewSet):
    queryset = CompanyEmployeeDetailsModel.objects.all()
    serializer_class = CompanyEmployeeDetailsModelSerializer


class CompanyEmployeeRoleManagementModelViewSet(viewsets.ModelViewSet):
    queryset = CompanyEmployeeRoleManagementModel.objects.all()
    serializer_class = CompanyEmployeeRoleManagementModelSerializer