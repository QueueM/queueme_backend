from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New Payment created: {instance.payment_id}")
        # Trigger additional actions (e.g., sending notifications) if needed.
