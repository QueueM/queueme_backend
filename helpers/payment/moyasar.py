import requests
import json


class Mayasar:
    """
    Moyasar Payment Gateway Integration

    This class provides an interface to interact with the Moyasar payment gateway.
    It allows creating payments, retrieving payment details, managing invoices, 
    and handling transactions securely.

    Attributes:
        api_key (str): The public API key for authentication.
        secret_key (str): The secret API key for authentication.
        callback_url (str): The URL where Moyasar will send payment status updates.
        _currency (str): The default currency for transactions (default: "SAR").
        _url (str): The base API URL for Moyasar.
        _payment_method (str): The default payment method (default: "creditcard").
        _auth (tuple): Authentication credentials for API requests.

    Methods:
        payment(amount, description, source):
            Initiates a payment transaction.
        get_payment():
            Retrieves all payment transactions.
        get_payment_by_id(payment_id):
            Retrieves a specific payment by its ID.
        invoice(amount, description, source):
            Creates an invoice.
        get_invoice():
            Retrieves all invoices.
        get_invoice_by_id(invoice_id):
            Retrieves a specific invoice by its ID.
    """

    def __init__(self, api_key: str, secret_key: str, callback_url: str) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.callback_url = callback_url
        self._currency = "SAR"
        self._url = "https://api.moyasar.com/v1"
        self._payment_method = "creditcard"
        self._auth = (self.secret_key, "")  # Use secret key for authentication

    def payment(self, amount, description, source):
        """Initiates a payment transaction."""
        try:
            payment_body = {
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
            response = requests.post(
                f"{self._url}/payments", headers=headers, data=json.dumps(payment_body), auth=self._auth
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_payment(self):
        """Retrieves all payment transactions."""
        try:
            response = requests.get(f"{self._url}/payments", auth=self._auth)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_payment_by_id(self, payment_id):
        """Retrieves a specific payment by its ID."""
        try:
            response = requests.get(f"{self._url}/payments/{payment_id}", auth=self._auth)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def invoice(self, amount, description, source):
        """Creates an invoice."""
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
            response = requests.post(
                f"{self._url}/invoices", headers=headers, data=json.dumps(invoice_body), auth=self._auth
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_invoice(self):
        """Retrieves all invoices."""
        try:
            response = requests.get(f"{self._url}/invoices", auth=self._auth)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_invoice_by_id(self, invoice_id):
        """Retrieves a specific invoice by its ID."""
        try:
            response = requests.get(f"{self._url}/invoices/{invoice_id}", auth=self._auth)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


