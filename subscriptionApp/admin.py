from django.contrib import admin
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel

# Inline for viewing subscribed companies on a plan’s change page.
class CompanySubscriptionDetailsInline(admin.TabularInline):
    model = CompanySubscriptionDetailsModel
    extra = 0
    readonly_fields = ['company']
    verbose_name_plural = "Subscribed Companies"

@admin.register(CompanySubscriptionPlansModel)
class CompanySubscriptionPlansAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "duration_days",
        "yearly_duration_days",
        "yearly_price",
        "services_limit",
        "bookings_limit",
        "specialists_limit",
        "branches_limit",
        "employees_limit",
        "subscription_count",
    ]
    fields = [
        "name",
        "description",
        "price",
        "duration_days",
        "yearly_duration_days",
        "yearly_price",
        "services_limit",
        "bookings_limit",
        "specialists_limit",
        "branches_limit",
        "employees_limit",
        "features",
    ]
    inlines = [CompanySubscriptionDetailsInline]

    def subscription_count(self, obj):
        # Assumes a related name of 'subscription_plan' on CompanySubscriptionDetailsModel
        return obj.subscription_plan.count()
    subscription_count.short_description = "Total Subscribed"
