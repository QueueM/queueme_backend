import requests
import json
import logging

logger = logging.getLogger(__name__)

class Moyasar:
    """
    Moyasar Payment Gateway Integration

    This class provides an interface to interact with the Moyasar payment gateway.
    It allows creating payments, retrieving payment details, managing invoices, 
    and handling transactions securely.

    Attributes:
        api_key (str): The public API key for authentication.
        secret_key (str): The secret API key for authentication.
        callback_url (str): The URL where Moyasar sends payment status updates.
        _currency (str): The default currency for transactions (SAR).
        _url (str): The base API URL for Moyasar.
        _payment_method (str): The default payment method (creditcard).
        _auth (tuple): Authentication credentials for API requests.
    """

    def __init__(self, api_key: str, secret_key: str, callback_url: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.callback_url = callback_url
        self._currency = "SAR"
        self._url = "https://api.moyasar.com/v1"
        self._payment_method = "creditcard"
        self._auth = (self.secret_key, "")  # Use secret key for HTTP Basic authentication

    def payment(self, amount, **kwargs):
        """
        Initiates a payment transaction.

        Keyword Args:
            source (dict): Payment source details.
            metadata (dict): Additional metadata to include in the transaction.
            description (str): Optional custom payment description.
        """
        try:
            source = kwargs.get("source", {})
            metadata = kwargs.get("metadata", {})
            description = kwargs.get("description", f'Plan {metadata.get("type", "payment")}')
            payment_body = {
                "amount": amount,
                "currency": self._currency,
                "description": description,
                "callback_url": self.callback_url,
                "metadata": metadata,
                "source": {
                    "type": self._payment_method,
                    **source
                },
            }
            headers = {"Content-Type": "application/json"}
            logger.info("Initiating payment with payload: %s", payment_body)
            response = requests.post(
                f"{self._url}/payments",
                headers=headers,
                data=json.dumps(payment_body),
                auth=self._auth
            )
            result = response.json()
            logger.info("Payment response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error initiating payment: %s", str(e))
            return {"error": str(e)}

    def get_payment(self):
        """Retrieves all payment transactions."""
        try:
            response = requests.get(f"{self._url}/payments", auth=self._auth)
            result = response.json()
            logger.info("Get payments response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error retrieving payments: %s", str(e))
            return {"error": str(e)}

    def get_payment_by_id(self, payment_id):
        """Retrieves a specific payment by its ID."""
        try:
            response = requests.get(f"{self._url}/payments/{payment_id}", auth=self._auth)
            result = response.json()
            logger.info("Get payment by ID response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error retrieving payment by ID: %s", str(e))
            return {"error": str(e)}

    def invoice(self, amount, description, source):
        """
        Creates an invoice.

        Args:
            amount (float): Invoice amount.
            description (str): Invoice description.
            source (dict): Source details for the invoice.
        """
        try:
            invoice_body = {
                "amount": amount,
                "currency": self._currency,
                "description": description,
                "callback_url": self.callback_url,
                "source": {
                    "type": self._payment_method,
                    **source,
                },
            }
            headers = {"Content-Type": "application/json"}
            logger.info("Creating invoice with payload: %s", invoice_body)
            response = requests.post(
                f"{self._url}/invoices",
                headers=headers,
                data=json.dumps(invoice_body),
                auth=self._auth
            )
            result = response.json()
            logger.info("Invoice creation response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error creating invoice: %s", str(e))
            return {"error": str(e)}

    def get_invoice(self):
        """Retrieves all invoices."""
        try:
            response = requests.get(f"{self._url}/invoices", auth=self._auth)
            result = response.json()
            logger.info("Get invoices response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error retrieving invoices: %s", str(e))
            return {"error": str(e)}

    def get_invoice_by_id(self, invoice_id):
        """Retrieves a specific invoice by its ID."""
        try:
            response = requests.get(f"{self._url}/invoices/{invoice_id}", auth=self._auth)
            result = response.json()
            logger.info("Get invoice by ID response: %s", result)
            return result
        except Exception as e:
            logger.exception("Error retrieving invoice by ID: %s", str(e))
            return {"error": str(e)}
