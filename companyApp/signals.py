"""
companyApp/signals.py

This module contains signal handlers for CompanyDetailsModel.
It updates AI-related fields (forecast_data and fraud_flag) after a company is saved
by using forecasting and fraud detection routines.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanyDetailsModel
from ai_features.forecasting import forecast_bookings
from ai_features.fraud_detection import detect_fraud  # detect_fraud is an alias for check_booking

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CompanyDetailsModel)
def update_company_ai(sender, instance, created, **kwargs):
    """
    Signal receiver that updates the forecast_data and fraud_flag fields of a CompanyDetailsModel
    instance after it is saved. An update query is used to avoid infinite recursion.
    
    It obtains:
      - forecast_data from forecast_bookings().
      - fraud_flag by passing the instance to detect_fraud().
    
    Any errors in these processes are caught and logged.
    """
    try:
        forecast_data = forecast_bookings()  # Adjust if parameters are needed
    except Exception as e:
        logger.error("Error forecasting bookings for Company ID %s: %s", instance.pk, e)
        forecast_data = {}

    try:
        # Pass the instance so that detect_fraud() receives the required argument.
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
    """
    Signal receiver to perform any necessary cleanup when a CompanyDetailsModel instance is deleted.
    """
    try:
        logger.info("Company ID %s was deleted. Cleanup actions can be performed here.", instance.pk)
        # Insert any cleanup logic if needed.
    except Exception as e:
        logger.error("Error during cleanup after deleting Company ID %s: %s", instance.pk, e)
