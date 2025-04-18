import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationModel
from customClasses.ai_utils import analyze_sentiment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=NotificationModel)
def enhance_notification_with_ai(sender, instance, created, **kwargs):
    """
    When a notification is created, analyze its sentiment and append an AI note if needed.
    """
    if created:
        try:
            sentiment_score = analyze_sentiment(instance.message)
            if sentiment_score is not None and sentiment_score < 0.4:
                instance.message += "\n[AI Note: Negative sentiment detected. Please review immediately.]"
                instance.save(update_fields=['message'])
                logger.debug(f"Enhanced Notification {instance.id} with AI note (sentiment={sentiment_score:.2f}).")
        except Exception as e:
            logger.error(f"Error enhancing notification {instance.id} with AI: {e}")
