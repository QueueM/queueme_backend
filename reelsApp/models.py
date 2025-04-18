# reelsApp/models.py
from django.db import models
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel
from django.utils import timezone

class ReelsModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, verbose_name="Shop", on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='reels/thumbnails/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    save_count = models.PositiveIntegerField(default=0)
    ai_video_tags = models.JSONField(blank=True, null=True, help_text="AI-generated tags for this video")
    processed_video_url = models.URLField(blank=True, null=True, help_text="URL for processed/transcoded video")
    analytics_data = models.JSONField(blank=True, null=True, help_text="Advanced analytics data")

    def like_count(self):
        return self.likes.count()

    def increment_views(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db(fields=['view_count'])

    def increment_shares(self):
        self.share_count = models.F('share_count') + 1
        self.save(update_fields=['share_count'])

    def increment_saves(self):
        self.save_count = models.F('save_count') + 1
        self.save(update_fields=['save_count'])

    def __str__(self):
        return f"Reel {self.id} - {self.caption[:20]}"

    class Meta:
        ordering = ['-created_at']

class CommentsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reel = models.ForeignKey(ReelsModel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def like_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment {self.id} on Reel {self.reel.id}"

class ReelsAnalytics(models.Model):
    reel = models.OneToOneField(ReelsModel, on_delete=models.CASCADE, related_name='analytics')
    average_watch_time = models.FloatField(default=0.0)
    drop_off_rate = models.FloatField(default=0.0)
    additional_data = models.JSONField(blank=True, null=True, help_text="Any additional analytics data")

    def __str__(self):
        return f"Analytics for Reel {self.reel.id}"
