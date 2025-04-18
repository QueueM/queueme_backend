# managers_auth_backend.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from usersapp.models import UserProfileModel
from authapp.models import SendOTPModel
from helpers.phone_utils import normalize_phone_number

User = get_user_model()

class ManagerPhoneBackend(ModelBackend):
    """
    Custom authentication backend for shop managers.
    It authenticates a user by:
      1. Normalizing the provided phone number.
      2. Verifying the OTP against SendOTPModel.
      3. Ensuring that a UserProfile exists with the normalized phone number.
      4. Checking that a ShopDetailsModel exists with that phone as its manager_phone_number.
    """
    def authenticate(self, request, phone_number=None, otp=None, **kwargs):
        if phone_number and otp:
            try:
                normalized_phone = normalize_phone_number(phone_number)
            except Exception:
                return None

            # Check OTP existence.
            if not SendOTPModel.objects.filter(otp=otp, phone_number=normalized_phone).exists():
                return None

            try:
                profile = UserProfileModel.objects.get(phone_number=normalized_phone)
                # Import ShopDetailsModel to verify manager phone.
                from shopApp.models import ShopDetailsModel
                if ShopDetailsModel.objects.filter(manager_phone_number=normalized_phone).exists():
                    return profile.user
            except UserProfileModel.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
