"""
subscriptionApp/models.py

This module defines the models used for handling user and company subscriptions, plans, 
and payment records.
"""

from django.db import models
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from django.utils.timezone import now
from django.utils import timezone


# ========== User Subscription Plans (not used in current logic) ==========
class UserSubscriptionPlansModels(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    duration = models.IntegerField()  # Duration in days

    def __str__(self):
        return self.name


class UserSubscriptionDetailsModel(models.Model):
    subscription_plan = models.OneToOneField(UserSubscriptionPlansModels, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# ========== Company Subscription Plans ==========
class CompanySubscriptionPlansModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()  # Monthly price
    duration_days = models.IntegerField()  # Duration in days (typically 30 for monthly)
    yearly_duration_days = models.IntegerField(default=365)  # Yearly duration (e.g., 365 days)
    yearly_price = models.FloatField(null=True, blank=True)  # Yearly price

    services_limit = models.IntegerField(null=True, blank=True)
    bookings_limit = models.IntegerField(null=True, blank=True)
    specialists_limit = models.IntegerField(null=True, blank=True)
    branches_limit = models.IntegerField(null=True, blank=True)
    employees_limit = models.IntegerField(null=True, blank=True)
    features = models.JSONField(default=dict)

    def __str__(self):
        return self.name


# ========== Payment ==========
class Payment(models.Model):
    class PayedForChoices(models.TextChoices):
        SUBSCRIPTION = 's', "Subscription"
        AD_SERVICE = "ad", "Ad Service"
        BOOKING = "b", "Booking"

    class PaymentTypeChoices(models.TextChoices):
        Payment = 'p', "Payment"
        Upgrade = "u", "Upgrade"

    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=1, choices=PaymentTypeChoices.choices)
    payed_for = models.CharField(max_length=3, choices=PayedForChoices.choices)
    creatd_at = models.DateTimeField(auto_now_add=True)

    # Billing Information
    bill_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    billing_cycle = models.CharField(
        max_length=10,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )

    def __str__(self):
        return self.payment_id


# ========== Company Subscription Details ==========
class CompanySubscriptionDetailsModel(models.Model):
    plan = models.ForeignKey(CompanySubscriptionPlansModel, on_delete=models.CASCADE, related_name='subscription_plan')
    company = models.OneToOneField(CompanyDetailsModel, on_delete=models.CASCADE, related_name='company')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)

    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    billing_cycle = models.CharField(
        max_length=10,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    ai_churn_data = models.JSONField(blank=True, null=True, help_text="AI churn prediction data")

    def save(self, *args, **kwargs):
        """
        Always update the start_date and end_date upon saving.
        The end_date is determined based on the billing_cycle and corresponding duration.
        """
        self.start_date = timezone.now()
        if self.billing_cycle == 'yearly':
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.yearly_duration_days)
        else:
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def _calculate_useused_days_price(self):
        """
        Calculates the unused portion of the subscription's price based on the remaining days.
        """
        remaining_days = (self.end_date - timezone.now()).days
        if remaining_days < 0:
            remaining_days = 0
        per_day_price = self.plan.price / self.plan.duration_days
        return per_day_price * remaining_days

    def have_to_pay(self, new_plan_price):
        """
        Determines if an upgrade requires extra payment.
        Returns the difference between the new plan's price and the current plan's price,
        or 0 if the new plan is cheaper.
        """
        if new_plan_price < self.plan.price:
            return 0
        return new_plan_price - self.plan.price

    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"
