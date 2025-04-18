# reelsApp/signals.py
import logging
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ReelsModel, CommentsModel
from notificationsapp.utils import create_notification, notify_followers

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ReelsModel)
def reel_created_notification(sender, instance, created, **kwargs):
    if created:
        title = "New Reel Posted"
        message = f"{instance.shop.shop_name} posted a new reel: {instance.caption[:50]}"
        notify_followers(instance.shop, title, message)

@receiver(post_save, sender=CommentsModel)
def comment_reply_notification(sender, instance, created, **kwargs):
    # If a comment is a reply, notify the parent comment's owner.
    if created and instance.parent and instance.parent.user != instance.user:
        title = "New Reply to Your Comment"
        message = f"Your comment on Reel {instance.reel.id} received a reply: {instance.text[:50]}"
        create_notification(instance.parent.user, title, message)

@receiver(m2m_changed, sender=CommentsModel.likes.through)
def comment_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_pk in pk_set:
            liker = User.objects.get(pk=user_pk)
            if liker != instance.user:
                title = "Your Comment was Liked"
                message = f"Your comment on Reel {instance.reel.id} was liked."
                create_notification(instance.user, title, message)
