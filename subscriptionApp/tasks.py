import logging
from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from subscriptionApp.models import CompanySubscriptionDetailsModel
from payment.services import initiate_payment

logger = logging.getLogger(__name__)

@shared_task
def process_recurring_payments():
    now = timezone.now()
    subscriptions = CompanySubscriptionDetailsModel.objects.filter(auto_renew=True, end_date__lte=now)
    logger.info("Found %d expired subscriptions for recurring processing.", subscriptions.count())
    for subscription in subscriptions:
        try:
            logger.info("Processing subscription ID %s for company %s", subscription.id, subscription.company.name)
            amount = subscription.plan.price  # Use yearly_price if billing_cycle is yearly
            # Retrieve stored payment token; adjust token retrieval as per your implementation.
            token = getattr(subscription.company, "payment_token", None)
            if not token:
                logger.error("No payment token for company %s; skipping subscription ID %s", subscription.company.name, subscription.id)
                continue
            source = {"token": token}
            metadata = {
                "subscription_id": subscription.id,
                "company_id": subscription.company.id,
                "bill_name": subscription.company.name,
                "billing_cycle": subscription.billing_cycle,
                "payment_type": "p"
            }
            payment_for = "subscription"
            result, payment_record = initiate_payment(payment_for, amount, source, metadata, "Recurring Subscription Payment")
            if result.get("status", "").lower() == "paid":
                subscription.renew()
                logger.info("Successfully renewed subscription ID %s for company %s", subscription.id, subscription.company.name)
            else:
                logger.warning("Recurring payment for subscription ID %s failed with status: %s", subscription.id, result.get("status"))
        except Exception as e:
            logger.exception("Error processing subscription ID %s: %s", subscription.id, e)
