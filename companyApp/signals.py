from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CompanyDetailsModel
from ai_features.forecasting import forecast_bookings
from ai_features.fraud_detection import detect_fraud

@receiver(post_save, sender=CompanyDetailsModel)
def update_company_ai(sender, instance, created, **kwargs):
    CompanyDetailsModel.objects.filter(pk=instance.pk).update(
        forecast_data=forecast_bookings(),
        fraud_flag=bool(detect_fraud())
    )
