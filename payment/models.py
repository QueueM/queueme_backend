# File: payment/models.py

from django.db import models

class Payment(models.Model):
    class PaymentForChoices(models.TextChoices):
        SUBSCRIPTION = 's', "Subscription"
        ADS = 'ad', "Ad Service"
        MERCHANT = 'm', "Merchant Payment"

    class PaymentTypeChoices(models.TextChoices):
        PAYMENT = 'p', "Payment"
        UPGRADE = 'u', "Upgrade"

    # A unique identifier for each payment transaction.
    payment_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=1, choices=PaymentTypeChoices.choices)
    # Renamed field: used to specify what the payment is for.
    payment_for = models.CharField(max_length=3, choices=PaymentForChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    bill_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    billing_cycle = models.CharField(
        max_length=10,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )

    def __str__(self) -> str:
        """
        Return a human-readable representation of the payment.
        Uses the auto-generated display method for the payment_for field.
        """
        return f"{self.payment_id} - {self.get_payment_for_display()}"
