from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone

# ignoreing
class UserSubscriptionPlansModels(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    duration = models.IntegerField() #Duration is in days

    def __str__(self):
        return self.name

# Ignoring
class UserSubscriptionDetailsModel(models.Model):
    subscription_plan = models.OneToOneField(UserSubscriptionPlansModels, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # plan = models.ForeignKey(SubscriptionPlansModels, on_delete=models.CASCADE)
    # company = models.OneToOneField(CompanyDetailsModel, on_delete=models.CASCADE)
    # start_date = models.DateTimeField(default=now)
    # end_date = models.DateTimeField()

    # def save(self, *args, **kwargs):
    #     if not self.end_date:
    #         self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
    #     super().save(*args, **kwargs)
    
    # def is_active(self):
    #     return self.end_date >= now()
    
    # def __str__(self):
    #     return f"{self.company.name} - {self.plan.name}"

# plan  Model 
class CompanySubscriptionPlansModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    duration_days = models.IntegerField() #Duration is in days
    services_limit = models.IntegerField(null=True, blank=True)
    bookings_limit = models.IntegerField(null=True, blank=True)
    specialists_limit = models.IntegerField(null=True, blank=True)
    branches_limit = models.IntegerField(null=True, blank=True)
    employees_limit = models.IntegerField(null=True, blank=True)
    features = models.JSONField(default=dict)  # Store additional features as JSON

    def __str__(self):
        return self.name



# Subscription Model for the company
class CompanySubscriptionDetailsModel(models.Model):
    plan = models.ForeignKey(CompanySubscriptionPlansModel, on_delete=models.CASCADE, related_name='subscription_plan')
    company = models.OneToOneField(CompanyDetailsModel, on_delete=models.CASCADE, related_name='company')
    payment_id = models.CharField(max_length=255 ,  null=True ,  blank=True )
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self,*args, **kwargs):
        if not  self.pk:
            self.start_date = timezone.now()
            self.end_date = self.start_date + timezone(days=self.plan.duration_days)
            return super().save(*args, **kwargs)
        
        
    def _calculate_useused_days_price(self):
            remaining_days = (self.end_date - timezone.now()).days
            if remaining_days < 0:
                remaining_days = 0  
            per_day_price = self.plan.price / self.plan.duration_days
            return per_day_price * remaining_days

    
    def have_to_pay(self ,new_plan_price):
        remaining_balance = self._calculate_unused_days_price()
        
        return new_plan_price - remaining_balance
        
    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"
        