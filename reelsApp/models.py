from django.db import models
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel

class ReelsModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, verbose_name="Reels", on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)  # Track who liked
    created_at = models.DateTimeField(auto_now_add=True)