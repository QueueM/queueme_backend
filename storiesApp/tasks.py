# storiesApp/tasks.py
import logging
from celery import shared_task
from ai_features.video_analysis import analyze_video_content
from ai_features.image_analysis import analyze_image  # Assuming a similar dummy function for images
from storiesApp.models import StoryModel

logger = logging.getLogger(__name__)

@shared_task
def process_story_media(story_id):
    """Asynchronously analyze story media (video or image) and update AI tags."""
    try:
        story = StoryModel.objects.get(pk=story_id)
        result = None
        if story.video:
            result = analyze_video_content(story)
        elif story.image:
            result = analyze_image(story.image)
        if result is not None:
            StoryModel.objects.filter(pk=story_id).update(ai_video_tags=result)
            logger.info(f"Processed media for story {story_id}, AI tags: {result}")
    except Exception as e:
        logger.error(f"Error processing media for story {story_id}: {e}")
