# notificationsapp/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotificationModel
from customClasses.ai_utils import analyze_sentiment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=NotificationModel)
def enhance_notification_with_ai(sender, instance, created, **kwargs):
    """
    After a NotificationModel is created, this signal handler uses AI-driven analysis
    to adjust the notification message based on the sentiment of its content.
    
    For example, if the sentiment is highly negative (indicating urgency or issues),
    an additional note is appended to the message.
    """
    if created:
        try:
            # Analyze the sentiment of the notification message.
            sentiment_score = analyze_sentiment(instance.message)
            # If the sentiment is low (e.g., below 0.4), append an extra note.
            if sentiment_score < 0.4:
                instance.message += "\n[AI Note: Negative sentiment detected. Please review immediately.]"
                instance.save(update_fields=['message'])
                logger.debug(f"Enhanced notification {instance.id} with AI note (sentiment score: {sentiment_score}).")
        except Exception as e:
            logger.error(f"Error enhancing notification {instance.id} with AI: {e}")
