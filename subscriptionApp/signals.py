


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CompanySubscriptionDetailsModel
from notificationsapp.models import NotificationModel

@receiver(post_save, sender=CompanySubscriptionDetailsModel)
def company_suscription_updated_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.company.user,  # Assuming Shop model has an owner field
            title="Subscription Started",
            message=f"Subscriptioin started for company {instance.company.name}"
        )
    else :
        NotificationModel.objects.create(
            user=instance.company.user,  # Assuming Shop model has an owner field
            title="Subscription Updated",
            message=f"Booking updated for company {instance.company.name}"
        )
