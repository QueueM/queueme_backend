import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanyDetailsModel
from ai_features.forecasting import forecast_bookings
from ai_features.fraud_detection import detect_fraud  # detect_fraud should be defined in your AI module

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CompanyDetailsModel)
def update_company_ai(sender, instance, created, **kwargs):
    try:
        forecast_data = forecast_bookings()  # You may pass parameters as needed
    except Exception as e:
        logger.error("Error forecasting bookings for Company ID %s: %s", instance.pk, e)
        forecast_data = {}

    try:
        fraud_flag = bool(detect_fraud(instance))
    except Exception as e:
        logger.error("Error detecting fraud for Company ID %s: %s", instance.pk, e)
        fraud_flag = False

    try:
        CompanyDetailsModel.objects.filter(pk=instance.pk).update(
            forecast_data=forecast_data,
            fraud_flag=fraud_flag
        )
        logger.info("Updated AI fields for Company ID %s: fraud_flag=%s", instance.pk, fraud_flag)
    except Exception as e:
        logger.error("Error updating CompanyDetailsModel for Company ID %s: %s", instance.pk, e)

@receiver(post_delete, sender=CompanyDetailsModel)
def cleanup_company_ai(sender, instance, **kwargs):
    try:
        logger.info("Company ID %s was deleted. Cleanup actions can be performed here.", instance.pk)
    except Exception as e:
        logger.error("Error during cleanup after deleting Company ID %s: %s", instance.pk, e)
