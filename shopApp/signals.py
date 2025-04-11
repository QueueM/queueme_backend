# shopApp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShopDetailsModel
from notificationsapp.models import NotificationModel
from customClasses.ai_utils import update_ai_fields

@receiver(post_save, sender=ShopDetailsModel)
def shop_created_or_updated_notification(sender, instance, created, **kwargs):
    """
    Create a notification when a shop is created or updated.
    """
    if created:
        title = "Shop Created"
        message = f"Shop '{instance.shop_name}' has been created."
    else:
        title = "Shop Updated"
        message = f"Shop '{instance.shop_name}' has been updated."
    
    NotificationModel.objects.create(
        user=instance.company.user,  # Assumes a related company with a user exists
        title=title,
        message=message
    )

@receiver(post_save, sender=ShopDetailsModel)
def update_ai_data(sender, instance, created, **kwargs):
    """
    Update the shop's AI recommendations and personalization data after save.
    """
    update_ai_fields(instance)
