# File: shopServiceApp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (ShopServiceDetailsModel,
                     ServiceBookingDiscountCouponsModel,
                     ServiceBookingDetailsModel)
from notificationsapp.utils import notify_followers
from customClasses.ai_utils import get_fraud_risk
from ai_features.forecasting import calculate_for_category, calculate_for_service

@receiver(post_save, sender=ShopServiceDetailsModel)
def service_created_notification(sender, instance, created, **kwargs):
    """
    Notify followers when a new service is created.
    """
    if created:
        title = "New Service Available"
        message = f"{instance.shop.shop_name} added a new service: {instance.name}"
        notify_followers(instance.shop, title, message)

@receiver(post_save, sender=ServiceBookingDiscountCouponsModel)
def discount_created_notification(sender, instance, created, **kwargs):
    """
    Notify followers when a new discount coupon is created.
    """
    if created:
        title = "New Discount Offer"
        message = f"{instance.shop.shop_name} is offering a discount: {instance.code}"
        notify_followers(instance.shop, title, message)

@receiver(post_save, sender=ServiceBookingDetailsModel)
def update_booking_fraud(sender, instance, created, **kwargs):
    """
    Calculate and update fraud flag for each booking.
    """
    try:
        risk_score = get_fraud_risk(instance)
        threshold = 0.7
        fraud_flag = risk_score > threshold
        if instance.fraud_flag != fraud_flag:
            instance.fraud_flag = fraud_flag
            instance.save(update_fields=['fraud_flag'])
    except Exception as e:
        print(f"Error updating fraud flag for booking {instance.id}: {e}")
