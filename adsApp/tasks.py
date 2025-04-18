import logging
from celery import shared_task
from customClasses.ai_utils import get_ai_recommendations
from .models import ShopAdsModel

logger = logging.getLogger(__name__)

@shared_task
def update_ad_ai_data(ad_id: int):
    """
    Celery task to compute and update AI targeting data for a ShopAd.
    Uses a direct update query to avoid triggering recursive signals.
    """
    try:
        ad = ShopAdsModel.objects.select_related('shop').get(pk=ad_id)
    except ShopAdsModel.DoesNotExist:
        logger.error(f"ShopAdsModel with id {ad_id} does not exist.")
        return
    try:
        ai_data = get_ai_recommendations(ad)
    except Exception as e:
        logger.exception(f"Exception in computing AI data for ad {ad_id}: {e}")
        ai_data = None
    # Update the ad's AI data without triggering save signals
    ShopAdsModel.objects.filter(pk=ad_id).update(ai_targeting_data=ai_data)
    logger.info(f"Ad {ad_id} AI targeting data updated: {ai_data}")
