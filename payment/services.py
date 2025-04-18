# File: payment/services.py

import logging
from typing import Tuple, Any, Dict
from .models import Payment
from .gateway import Moyasar

logger = logging.getLogger(__name__)

def get_payment_for_code(payment_for: str) -> str:
    """
    Maps a payment type (e.g., 'subscription', 'ads', or 'merchant') 
    to its corresponding code. This code is stored in the Payment model.

    Args:
        payment_for (str): The descriptive payment type.

    Returns:
        str: The corresponding code ('s', 'ad', or 'm').
    """
    mapping = {
        "subscription": "s",
        "ads": "ad",
        "merchant": "m"
    }
    return mapping.get(payment_for, "s")

def initiate_payment(payment_for: str, amount: Any, source: dict, metadata: dict,
                     description: str = "") -> Tuple[Dict, Payment]:
    """
    Initiates a payment transaction using the Moyasar gateway.
    Saves or updates the Payment record using the new field name 'payment_for'.

    Args:
        payment_for (str): A descriptor for what the payment is for (e.g., "subscription").
        amount (Any): The amount to charge.
        source (dict): Payment source details (e.g., credit card info).
        metadata (dict): Additional metadata; must contain key "payment_for" under new logic.
        description (str, optional): A description for the transaction.

    Returns:
        Tuple[Dict, Payment]: A tuple containing the response from Moyasar and the Payment model instance.
    """
    try:
        moyasar = Moyasar(wallet=payment_for)
        result = moyasar.payment(amount=amount, source=source, metadata=metadata, description=description)
        
        # Get the appropriate payment code based on the descriptive payment_for input.
        pay_code = get_payment_for_code(payment_for)
        payment_id_val = result.get("id", "")
        
        payment_record, created = Payment.objects.update_or_create(
            payment_id=payment_id_val,
            defaults={
                "amount": amount,
                "status": result.get("status", ""),
                "payment_type": metadata.get("payment_type", "p"),
                "payment_for": pay_code,  # New field name used here.
                "bill_name": metadata.get("bill_name", ""),
                "phone_number": metadata.get("phone_number", ""),
                "email": metadata.get("email", ""),
                "address": metadata.get("address", ""),
                "billing_cycle": metadata.get("billing_cycle", "monthly"),
            }
        )
        logger.info("Payment record created or updated: %s", payment_record)
        return result, payment_record
    except Exception as e:
        logger.exception("Error initiating payment: %s", e)
        raise e

def process_payment_callback(payment_id: str, wallet_type: str) -> Dict:
    """
    Processes a payment callback by querying the Moyasar gateway for the current status.

    Args:
        payment_id (str): The identifier of the payment transaction.
        wallet_type (str): The wallet type (used to instantiate the proper Moyasar instance).

    Returns:
        Dict: The response from the Moyasar gateway.
    """
    try:
        moyasar = Moyasar(wallet=wallet_type)
        result = moyasar.get_payment_by_id(payment_id)
        payment_record = Payment.objects.filter(payment_id=payment_id).first()

        if payment_record:
            payment_record.status = result.get("status", payment_record.status)
            payment_record.save()

        logger.info("Processed payment callback for %s: %s", payment_id, result)
        return result
    except Exception as e:
        logger.exception("Error processing payment callback: %s", e)
        raise e
