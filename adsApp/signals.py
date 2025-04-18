import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ShopAdsModel
from customClasses.ai_utils import get_ai_recommendations

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ShopAdsModel)
def update_ad_ai_data(sender, instance, created, **kwargs):
    try:
        ai_data = get_ai_recommendations(instance)
        if ai_data:
            logger.debug(f"AI targeting data for ad {instance.id}: {ai_data}")
            instance.ai_targeting_data = ai_data
            instance.save(update_fields=["ai_targeting_data"])
    except Exception as e:
        logger.error(f"Error updating AI data for ad {instance.id}: {e}")
