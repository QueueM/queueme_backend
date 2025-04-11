# companyApp/views.py
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from authapp.models import SendOTPModel
from usersapp.models import UserProfileModel
from .models import CompanyDetailsModel
from .serializers import CompanyDetailsModelSerializer
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CompanyDetailsFilter  # Import your custom filter

from ai_features.forecasting import forecast_bookings
from ai_features.fraud_detection import detect_fraud

class RegisterAsCompanyAPIView(APIView):
    permission_classes = []  # Adjust permissions as needed

    def post(self, request):
        required_fields = ['username', 'company_name', 'name', 'phone_number', 'password', 'otp']
        missing = [field for field in required_fields if field not in request.data]
        if missing:
            return Response(
                {'message': f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp = request.data['otp']
        phone = request.data['phone_number']
        if not SendOTPModel.objects.filter(otp=otp, phone_number=phone).exists():
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user.
        user = User(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()

        # Create the user profile.
        UserProfileModel.objects.create(user=user, name=request.data['name'], phone_number=phone)

        # Create the company.
        company = CompanyDetailsModel.objects.create(user=user, name=request.data['company_name'])
        # Immediately update AI fields.
        CompanyDetailsModel.objects.filter(pk=company.pk).update(
            forecast_data=forecast_bookings(),
            fraud_flag=bool(detect_fraud())
        )

        # Clean up OTP records.
        SendOTPModel.objects.filter(otp=otp, phone_number=phone).delete()

        serializer = CompanyDetailsModelSerializer(company, context={'user': user})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CompanyDetailsViewSet(CustomBaseModelViewSet):
    queryset = CompanyDetailsModel.objects.all()
    serializer_class = CompanyDetailsModelSerializer

    # Integrate filtering, searching, and ordering.
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompanyDetailsFilter
    search_fields = ['name', 'contact_email']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        # Limit companies to the authenticated user.
        return CompanyDetailsModel.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
