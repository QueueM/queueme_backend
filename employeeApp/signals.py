import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeDetailsModel
from ai_features.employee_performance import calculate_employee_performance

logger = logging.getLogger(__name__)

@receiver(post_save, sender=EmployeeDetailsModel)
def update_employee_performance(sender, instance, created, **kwargs):
    try:
        performance_data = calculate_employee_performance(instance)
        EmployeeDetailsModel.objects.filter(pk=instance.pk).update(ai_performance_data=performance_data)
        logger.debug("Updated AI performance data for employee %s: %s", instance.pk, performance_data)
    except Exception as e:
        logger.error("Error updating AI performance data for employee %s: %s", instance.pk, e)
