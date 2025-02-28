

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ShopDetailsModel
from notificationsapp.models import NotificationModel

@receiver(post_save, sender=ShopDetailsModel)
def shop_created_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.company.user,  # Assuming Shop model has an owner field
            title="Shop Created",
            message=f"Shop '{instance.name}' was created."
        )
    else :
        NotificationModel.objects.create(
            user=instance.company.user,  # Assuming Shop model has an owner field
            title="Shop Updated",
            message=f"Shop '{instance.name}' was updated."
        )
