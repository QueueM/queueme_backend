from django.shortcuts import render

# Create your views here.
import random
from .models import SendOTPModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendOTPModelSerializer

from django.contrib.auth.models import User

class RegistrationOTPAPIView(APIView):
    permission_classes = []
    def get(self, request):

        required_keys = ['phone_number', 'otp_type']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.GET]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # otp = random.randint(100000, 999999)
        otp = 1
        phone_number = request.GET["phone_number"]
        type = request.GET['otp_type']
        otpRecord = SendOTPModel(phone_number=phone_number, otp=otp, otp_type=type, otp_mode='phone')
        # serializer = SendOTPModelSerializer(data = {"phone_number":phone_number, "otp":otp, "otp_type":type, "otp_mode":"phone"} )
        
        oldOTP = SendOTPModel.objects.filter(phone_number=phone_number)
        if oldOTP.exists():
            oldOTP.delete()

        otpRecord.save()
        serializer = SendOTPModelSerializer(otpRecord)
        return Response({"message":"OTP sent successfully"})



class TestAPIView(APIView):
    permission_classes = []
    def get(self, request):
        return Response({"namse":"Aman Ansari"})
    
    
class ResetPasswordAPIView(APIView):
    permission_classes = []
    def post(self, request):
        # Parse the request body (DRF automatically parses JSON into `request.data`)
        required_keys = ['username', 'new_password', 'otp', 'phone_number']
        
        # Validate required keys
        missing_keys = [key for key in required_keys if key not in request.data]
        if missing_keys:
            return Response(
                {"message": f"Missing required field(s): {', '.join(missing_keys)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # getting data
        username = request.data['username']
        password = request.data['new_password']
        otp = request.data['otp']
        phoneNumber = request.data['phone_number']

        # check if user exist
        user = User.objects.filter(username=username)
        if not user.exists():
            return Response({"message" : "User with same username does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        # Check otp validation
        otpRecord = SendOTPModel.objects.filter(otp=otp, phone_number=phoneNumber)
        if not otpRecord.exists():
            return Response({"message" : "Invalid OTP !!"},status=status.HTTP_400_BAD_REQUEST)
        
        # create user
        user = User(username=username)
        user.set_password(password)
        user.save()
        
        # Delete otp
        otpRecord.delete()
        return Response({"message":"Password updated sucessfully"},status=status.HTTP_200_OK)