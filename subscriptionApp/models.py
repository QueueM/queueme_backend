from django.db import models
from django.utils import timezone
from companyApp.models import CompanyDetailsModel

# Company Subscription Plans
class CompanySubscriptionPlansModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()  # Monthly price
    duration_days = models.IntegerField()  # E.g., 30 for monthly
    yearly_duration_days = models.IntegerField(default=365)
    yearly_price = models.FloatField(null=True, blank=True)

    services_limit = models.IntegerField(null=True, blank=True)
    bookings_limit = models.IntegerField(null=True, blank=True)
    specialists_limit = models.IntegerField(null=True, blank=True)
    branches_limit = models.IntegerField(null=True, blank=True)
    employees_limit = models.IntegerField(null=True, blank=True)
    features = models.JSONField(default=dict)

    def __str__(self):
        return self.name

# Company Subscription Details
class CompanySubscriptionDetailsModel(models.Model):
    plan = models.ForeignKey(CompanySubscriptionPlansModel, on_delete=models.CASCADE, related_name='subscription_plan')
    company = models.OneToOneField(CompanyDetailsModel, on_delete=models.CASCADE, related_name='company')
    # Reference to Payment record if available.
    payment = models.ForeignKey("payment.Payment", on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    billing_cycle = models.CharField(
        max_length=10,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    auto_renew = models.BooleanField(default=True)
    ai_churn_data = models.JSONField(blank=True, null=True, help_text="AI churn prediction data")

    def save(self, *args, **kwargs):
        self.start_date = timezone.now()
        if self.billing_cycle == 'yearly':
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.yearly_duration_days)
        else:
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def renew(self):
        if self.billing_cycle == 'yearly':
            extension = timezone.timedelta(days=self.plan.yearly_duration_days)
        else:
            extension = timezone.timedelta(days=self.plan.duration_days)
        self.start_date = self.end_date
        self.end_date += extension
        self.save()

    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"
