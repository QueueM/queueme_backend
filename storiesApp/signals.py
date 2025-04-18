# storiesApp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoryModel
from notificationsapp.utils import notify_followers

@receiver(post_save, sender=StoryModel)
def story_created_notification(sender, instance, created, **kwargs):
    if created:
        title = "New Story Posted"
        message = f"{instance.shop.shop_name} posted a new story."
        notify_followers(instance.shop, title, message)
