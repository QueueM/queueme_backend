# storiesApp/models.py
from django.db import models
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel
from django.utils import timezone
from datetime import timedelta

class StoryModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, verbose_name="Shop", on_delete=models.CASCADE)
    video = models.FileField(upload_to='stories/videos/', null=True, blank=True)
    image = models.ImageField(upload_to='stories/images/', null=True, blank=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True, help_text="Story expires 24 hours after creation")
    view_count = models.PositiveIntegerField(default=0)
    viewed_by = models.ManyToManyField(User, related_name='viewed_stories', blank=True)
    ai_video_tags = models.JSONField(blank=True, null=True, help_text="AI-generated tags for story video")
    analytics_data = models.JSONField(blank=True, null=True, help_text="Advanced analytics data")

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def increment_views(self):
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db(fields=['view_count'])

    def is_expired(self):
        return timezone.now() >= self.expires_at

    def __str__(self):
        return f"Story {self.id} by {self.shop}"

    class Meta:
        ordering = ['-created_at']

class StoryViewedModel(models.Model):
    story = models.ForeignKey(StoryModel, on_delete=models.CASCADE, related_name="views_detail")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')

    def __str__(self):
        return f"View of Story {self.story.id} by {self.user.username}"
