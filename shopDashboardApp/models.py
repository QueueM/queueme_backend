# shopDashboardApp/models.py
from django.db import models
from django.utils import timezone
from shopApp.models import ShopDetailsModel
from companyApp.models import CompanyDetailsModel

class DashboardLog(models.Model):
    timestamp               = models.DateTimeField(default=timezone.now)
    company                 = models.ForeignKey(CompanyDetailsModel, on_delete=models.CASCADE)
    shop                    = models.ForeignKey(ShopDetailsModel, null=True, blank=True, on_delete=models.CASCADE)
    total_bookings          = models.IntegerField(default=0)
    total_revenue           = models.FloatField(default=0.0)
    total_specialists       = models.IntegerField(default=0)
    total_waiting           = models.IntegerField(default=0)
    total_in_progress       = models.IntegerField(default=0)
    total_completed         = models.IntegerField(default=0)
    total_cancelled         = models.IntegerField(default=0)
    estimated_wait_time     = models.CharField(max_length=50, default="0 minutes")
    total_employees         = models.IntegerField(default=0)
    average_salary          = models.FloatField(default=0.0)
    total_customers         = models.IntegerField(default=0)
    customer_retention_rate = models.FloatField(default=0.0)
    average_rating          = models.FloatField(default=0.0)
    total_reels_likes       = models.IntegerField(default=0)
    total_ad_impressions    = models.IntegerField(default=0)
    total_ad_viewers        = models.IntegerField(default=0)
    total_ad_clicks         = models.IntegerField(default=0)
    top_services            = models.JSONField(default=list)
    
    # New fields for stories and reels:
    total_stories           = models.IntegerField(default=0)
    total_story_likes       = models.IntegerField(default=0)
    total_reels             = models.IntegerField(default=0)
    total_comments_per_reel = models.IntegerField(default=0)  # Changed to integer field

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"DashboardLog ({self.id}) - {self.timestamp}"
