# shopServiceApp/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import Signal, receiver
from .models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel
)
from ai_features.forecasting import calculate_for_category, calculate_for_service
from customClasses.ai_utils import get_fraud_risk

booking_changed = Signal()

@receiver(post_save, sender=ShopServiceCategoryModel)
def update_category_forecast(sender, instance, created, **kwargs):
    try:
        data = calculate_for_category(instance)
        ShopServiceCategoryModel.objects.filter(pk=instance.pk).update(forecast_data=data)
    except Exception as e:
        print(f"Error updating forecast for category {instance.pk}: {e}")

@receiver(post_save, sender=ShopServiceDetailsModel)
def update_service_forecast(sender, instance, created, **kwargs):
    try:
        data = calculate_for_service(instance)
        ShopServiceDetailsModel.objects.filter(pk=instance.pk).update(forecast_data=data)
    except Exception as e:
        print(f"Error updating forecast for service {instance.pk}: {e}")

@receiver(post_save, sender=ServiceBookingDetailsModel)
def emit_booking_created_or_updated(sender, instance, created, **kwargs):
    booking_changed.send(sender=sender, instance=instance, created=created, deleted=False)

@receiver(post_delete, sender=ServiceBookingDetailsModel)
def emit_booking_deleted(sender, instance, **kwargs):
    booking_changed.send(sender=sender, instance=instance, created=False, deleted=True)

@receiver(post_save, sender=ServiceBookingDetailsModel)
def update_booking_fraud(sender, instance, created, **kwargs):
    try:
        risk_score = get_fraud_risk(instance)
        threshold = 0.7
        fraud_flag = risk_score > threshold
        if instance.fraud_flag != fraud_flag:
            instance.fraud_flag = fraud_flag
            instance.save(update_fields=['fraud_flag'])
    except Exception as e:
        print(f"Error updating fraud flag for booking {instance.id}: {e}")
