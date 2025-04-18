# File: payment/gateway.py

import requests
import json
import logging
from decouple import config

logger = logging.getLogger(__name__)

class Moyasar:
    """
    Integration with the Moyasar API.
    
    Wallet types:
      - "subscription"
      - "ads"
      - "merchant"
    
    Ensure your environment variables are set:
      For subscription: MOYASAR_PUBLIC_SUBSCRIPTIONS, MOYASAR_SECRET_SUBSCRIPTIONS, MOYASAR_CALLBACK_URL_SUBSCRIPTIONS
      For ads: MOYASAR_PUBLIC_ADS, MOYASAR_SECRET_ADS, MOYASAR_CALLBACK_URL_ADS
      For merchant: MOYASAR_PUBLIC_MERCHANT, MOYASAR_SECRET_MERCHANT, MOYASAR_CALLBACK_URL_MERCHANT
    """
    def __init__(self, wallet: str) -> None:
        if wallet == "subscription":
            self.api_key = config("MOYASAR_PUBLIC_SUBSCRIPTIONS", default="")
            self.secret_key = config("MOYASAR_SECRET_SUBSCRIPTIONS", default="")
            self.callback_url = config("MOYASAR_CALLBACK_URL_SUBSCRIPTIONS", default="")
        elif wallet == "ads":
            self.api_key = config("MOYASAR_PUBLIC_ADS", default="")
            self.secret_key = config("MOYASAR_SECRET_ADS", default="")
            self.callback_url = config("MOYASAR_CALLBACK_URL_ADS", default="")
        elif wallet == "merchant":
            self.api_key = config("MOYASAR_PUBLIC_MERCHANT", default="")
            self.secret_key = config("MOYASAR_SECRET_MERCHANT", default="")
            self.callback_url = config("MOYASAR_CALLBACK_URL_MERCHANT", default="")
        else:
            raise ValueError("Invalid wallet type provided.")

        self._currency = "SAR"
        self._url = "https://api.moyasar.com/v1"
        self._payment_method = "creditcard"
        self._auth = (self.secret_key, "")

    def payment(self, amount, **kwargs):
        """
        Initiates a payment via Moyasar.
        
        Parameters:
          amount: Payment amount in minor units (e.g. 9900 for 99.00 SAR).
          kwargs: Must include:
                   - source: Payment source details (credit card info).
                   - metadata: Must include "payment_for" with the appropriate value ("s", "ad", "m").
                   - description: Optional payment description.
                   
        Returns: JSON result from Moyasar.
        """
        try:
            source = kwargs.get("source", {})
            metadata = kwargs.get("metadata", {})
            description = kwargs.get("description", f"Payment for {metadata.get('type', 'payment')}")
            payload = {
                "amount": amount,
                "currency": self._currency,
                "description": description,
                "callback_url": self.callback_url,
                "metadata": metadata,
                "source": {
                    "type": self._payment_method,
                    "name": source.get("name", ""),
                    "number": source.get("number", ""),
                    "cvc": source.get("cvc", ""),
                    "month": source.get("month", ""),
                    "year": source.get("year", ""),
                    "3ds": source.get("3ds", True),
                    "manual": source.get("manual", False),
                    "save_card": source.get("save_card", False)
                }
            }
            headers = {"Content-Type": "application/json"}
            logger.info("Initiating Moyasar payment with payload: %s", payload)
            response = requests.post(f"{self._url}/payments", headers=headers, data=json.dumps(payload), auth=self._auth)
            result = response.json()
            logger.info("Moyasar payment response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error initiating payment: %s", str(e))
            return {"error": str(e)}

    def get_payment_by_id(self, payment_id):
        """
        Retrieves payment details from Moyasar.
        """
        try:
            response = requests.get(f"{self._url}/payments/{payment_id}", auth=self._auth)
            result = response.json()
            logger.info("Retrieved payment by ID %s: %s", payment_id, result)
            return result
        except Exception as e:
            logger.exception("Error retrieving payment by ID: %s", str(e))
            return {"error": str(e)}
