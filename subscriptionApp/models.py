from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from django.utils.timezone import now
from datetime import timedelta

class UserSubscriptionPlansModels(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    duration = models.IntegerField() #Duration is in days

    def __str__(self):
        return self.name


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
    
class CompanySubscriptionPlansModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    duration_days = models.IntegerField() #Duration is in days

    def __str__(self):
        return self.name

class CompanySubscriptionDetailsModel(models.Model):
    plan = models.ForeignKey(CompanySubscriptionPlansModel, on_delete=models.CASCADE, related_name='subscription_plan')
    company = models.OneToOneField(CompanyDetailsModel, on_delete=models.CASCADE, related_name='company')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)
    
    def is_active(self):
        return self.end_date >= now()
    
    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"