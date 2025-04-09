# reelsApp/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReelsModel, StoryModel
from ai_features.video_analysis import analyze_video_content

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ReelsModel)
def analyze_reel_video(sender, instance, created, **kwargs):
    """
    When a new reel is saved, analyze its video content using AI and update the ai_video_tags field.
    """
    if created and instance.video:
        try:
            # Analyze the reel video using our AI function
            analysis = analyze_video_content(instance)
            instance.ai_video_tags = analysis
            # Save without triggering the signal recursion by updating only the ai_video_tags field
            instance.save(update_fields=['ai_video_tags'])
            logger.debug("Updated AI video tags for reel %s: %s", instance.pk, analysis)
        except Exception as e:
            logger.error("Error analyzing reel video for instance %s: %s", instance.pk, e)

@receiver(post_save, sender=StoryModel)
def analyze_story_video(sender, instance, created, **kwargs):
    """
    When a new story is saved, analyze its video content using AI and update the ai_video_tags field.
    """
    if created and instance.video:
        try:
            analysis = analyze_video_content(instance)
            instance.ai_video_tags = analysis
            instance.save(update_fields=['ai_video_tags'])
            logger.debug("Updated AI video tags for story %s: %s", instance.pk, analysis)
        except Exception as e:
            logger.error("Error analyzing story video for instance %s: %s", instance.pk, e)
