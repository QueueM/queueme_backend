# reviewApp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from customClasses.ai_utils import analyze_sentiment

@receiver(post_save, sender=Review)
def update_review_sentiment(sender, instance, created, **kwargs):
    """
    Analyze the sentiment of a review after it is saved and update its sentiment_score.
    """
    if instance.comment:
        sentiment = analyze_sentiment(instance.comment)
        # Update the sentiment_score only if it changes to avoid recursion.
        if instance.sentiment_score != sentiment:
            instance.sentiment_score = sentiment
            instance.save(update_fields=['sentiment_score'])
