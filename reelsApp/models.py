# reelsApp/models.py
from django.db import models
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel

class ReelsModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, verbose_name="Shop", on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)  # Track who liked
    created_at = models.DateTimeField(auto_now_add=True)
    ai_video_tags = models.JSONField(blank=True, null=True, help_text="AI generated tags for reel video")

    def like_count(self):
        return self.likes.count()

class CommentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey(ReelsModel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)  # Track who liked
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def like_count(self):
        return self.likes.count()

    def is_reply(self):
        return self.parent is not None

class StoryModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, verbose_name="Shop", on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    created_at = models.DateTimeField(auto_now_add=True)
    ai_video_tags = models.JSONField(blank=True, null=True, help_text="AI generated tags for story video")

class StoryViewedModel(models.Model):
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewd_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')  # Ensure a user can't view a story multiple times
