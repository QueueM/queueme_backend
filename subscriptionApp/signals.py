"""
subscriptionApp/signals.py

Signals to handle post-save events for subscription details.
Creates notifications and updates AI churn prediction data upon subscription updates.
"""

import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanySubscriptionDetailsModel
from notificationsapp.models import NotificationModel
from ai_features.churn_prediction import calculate_churn_risk

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CompanySubscriptionDetailsModel)
def company_subscription_updated_notification(sender, instance, created, **kwargs):
    """
    Sends a notification when a subscription is created or updated,
    and updates AI churn prediction data.
    """
    try:
        if created:
            NotificationModel.objects.create(
                user=instance.company.user,
                title="Subscription Started",
                message=f"Subscription started for company {instance.company.name}"
            )
        else:
            NotificationModel.objects.create(
                user=instance.company.user,
                title="Subscription Updated",
                message=f"Subscription updated for company {instance.company.name}"
            )
        
        # Update AI churn prediction data.
        ai_data = calculate_churn_risk(instance)
        CompanySubscriptionDetailsModel.objects.filter(pk=instance.pk).update(ai_churn_data=ai_data)
        logger.debug("Updated AI churn data for subscription %s: %s", instance.pk, ai_data)
    except Exception as e:
        logger.error("Error updating AI churn data for subscription %s: %s", instance.pk, e)
