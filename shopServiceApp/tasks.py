# shopServiceApp/tasks.py
from celery import shared_task
import logging

from .models import ShopServiceCategoryModel, ShopServiceDetailsModel
from ai_features.forecasting import calculate_for_category, calculate_for_service

logger = logging.getLogger(__name__)

@shared_task
def recalc_category_forecasts():
    """
    Recalculate AI forecasts for all service categories.
    """
    for category in ShopServiceCategoryModel.objects.all():
        try:
            data = calculate_for_category(category)
            category.forecast_data = data
            category.save(update_fields=['forecast_data'])
        except Exception as e:
            logger.error(f"Error updating forecast for category {category.pk}: {e}")

@shared_task
def recalc_service_forecasts():
    """
    Recalculate AI forecasts for all services.
    """
    for service in ShopServiceDetailsModel.objects.all():
        try:
            data = calculate_for_service(service)
            service.forecast_data = data
            service.save(update_fields=['forecast_data'])
        except Exception as e:
            logger.error(f"Error updating forecast for service {service.pk}: {e}")

@shared_task
def recalc_all_forecasts():
    """
    Trigger both category and service forecast recalculations.
    """
    recalc_category_forecasts.delay()
    recalc_service_forecasts.delay()
