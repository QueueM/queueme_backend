from django.db import models
from shopApp.models import ShopDetailsModel
from shopServiceApp.models import ShopServiceDetailsModel
from django.utils.timezone import now
from django.contrib.auth.models import User

class ShopAdsModel(models.Model):
    shop = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE)
    service = models.ForeignKey(ShopServiceDetailsModel, on_delete=models.CASCADE, null=True)
    target_gender = models.CharField(max_length=200, choices=ShopDetailsModel.TARGET_CUSTOMER_CHOICES.choices)
    title = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='images/ads/cover', null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text="Total budget for the ad")
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ai_targeting_data = models.JSONField(blank=True, null=True, help_text="AI targeting metadata for this ad")

    def deduct_budget(self, views_count=1):
        cost_per_view = 1
        total_deduction = cost_per_view * views_count
        self.budget -= total_deduction
        self.shop.credits -= 1
        if self.budget <= 0:
            self.budget = 0
            self.is_active = False
            return False
        self.save()
        return True

class ShopAdsImpressionModel(models.Model):
    class IMPRESSION_TYPES(models.TextChoices):
        CLICK = 'click', 'Click'
        VIEW  = 'view',  'View'

    ad = models.ForeignKey(ShopAdsModel, on_delete=models.CASCADE, related_name='impressions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    impression_type = models.CharField(
        max_length=10,
        choices=IMPRESSION_TYPES.choices,
        default=IMPRESSION_TYPES.VIEW
    )
    timestamp = models.DateTimeField(auto_now_add=True)