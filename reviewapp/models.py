# reviewApp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Review(models.Model):
    # The user who left the review.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Review fields.
    title = models.CharField(max_length=255, help_text="Short title for the review")
    rating = models.PositiveSmallIntegerField(help_text="Rating (1 to 5 stars)")
    comment = models.TextField(blank=True, null=True, help_text="Detailed review text")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic relation to any object (e.g., shop, service, or specialist).
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Field for the AI sentiment score.
    sentiment_score = models.FloatField(blank=True, null=True, help_text="Sentiment analysis score")
    
    def __str__(self):
        return f"{self.title} by {self.user}"
    
    class Meta:
        ordering = ['-created_at']
