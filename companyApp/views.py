from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from authapp.models import SendOTPModel
from usersapp.models import UserProfileModel

from .models import CompanyDetailsModel
from .serializers import CompanyDetailsModelSerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet

# Import AI modules from their actual filenames
from ai_features.forecasting import forecast_bookings
from ai_features.fraud_detection import detect_fraud

class RegisterAsCompanyAPIView(APIView):
    permission_classes = []

    def post(self, request):
        required = ['username','company_name','name','phone_number','password','otp']
        missing = [k for k in required if k not in request.data]
        if missing:
            return Response({'message': f"Missing fields: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)

        otp = request.data['otp']
        phone = request.data['phone_number']
        if not SendOTPModel.objects.filter(otp=otp, phone_number=phone).exists():
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        UserProfileModel.objects.create(user=user, name=request.data['name'], phone_number=phone)

        company = CompanyDetailsModel.objects.create(user=user, name=request.data['company_name'])
        # Immediately update AI fields
        CompanyDetailsModel.objects.filter(pk=company.pk).update(
            forecast_data=forecast_bookings(),
            fraud_flag=bool(detect_fraud())
        )

        SendOTPModel.objects.filter(otp=otp, phone_number=phone).delete()
        serializer = CompanyDetailsModelSerializer(company, context={'user': user})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CompanyDetailsViewSet(CustomBaseModelViewSet):
    queryset = CompanyDetailsModel.objects.all()
    serializer_class = CompanyDetailsModelSerializer

    def get_queryset(self):
        return CompanyDetailsModel.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['user'] = self.request.user
        return ctx
