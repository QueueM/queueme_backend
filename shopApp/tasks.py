# shopApp/tasks.py
import logging
from celery import shared_task
from customClasses.ai_utils import get_ai_recommendations, get_ai_personalization
from shopApp.models import ShopDetailsModel

logger = logging.getLogger(__name__)

@shared_task
def update_shop_ai_fields(shop_id):
    """Asynchronously compute and update AI recommendation/personalization for a shop."""
    try:
        shop = ShopDetailsModel.objects.get(pk=shop_id)
        recs = get_ai_recommendations(shop)
        pers = get_ai_personalization(shop)
        ShopDetailsModel.objects.filter(pk=shop_id).update(ai_recommendations=recs, ai_personalization=pers)
        logger.info(f"Updated AI fields for Shop {shop_id}")
    except Exception as e:
        logger.error(f"Error updating AI fields for Shop {shop_id}: {e}")
