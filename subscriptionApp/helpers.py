from django.utils import timezone
from .models import CompanySubscriptionDetailsModel

def create_subscription(company, plan, billing_cycle="monthly"):
    if not company.is_active:
        raise ValueError("Company is inactive, cannot create a subscription.")
    
    if billing_cycle == "yearly":
        if not plan.yearly_price or not plan.yearly_duration_days:
            raise ValueError("Yearly pricing information is missing for this plan.")
        duration = plan.yearly_duration_days
    else:
        duration = plan.duration_days

    subscription = CompanySubscriptionDetailsModel.objects.create(
        company=company,
        plan=plan,
        billing_cycle=billing_cycle,
        start_date=timezone.now(),
        end_date=timezone.now() + timezone.timedelta(days=duration)
    )
    return subscription
