from django.db import models

# Create your models here.


class SendOTPModel(models.Model):
    OTP_TYPE_CHOICES = [
        ('login', 'Login'),
        ('register', 'Register'),
        ('reset_password', 'Reset password'),
    ]
    OTP_MODE_CHOICES = [
        ('phone', 'Available'),
        ('email', 'Driving')
    ]
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=20)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES, default="login")
    otp_mode = models.CharField(max_length=20, choices=OTP_MODE_CHOICES, default='phone')