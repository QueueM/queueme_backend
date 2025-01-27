

from datetime import datetime
from django.utils.timezone import now
from .models import CompanySubscriptionDetailsModel
def create_subscription(company, plan):
    if not company.is_active:
        raise ValueError("Company is inactive, cannot create a subscription.")
    
    subscription = CompanySubscriptionDetailsModel.objects.create(
        company=company,
        plan=plan,
        start_date=now()
    )
    return subscription