from django.db import models


class Payment(models.Model):

    PAYMENT_TYPE_CHOICES = (
        ('card', 'Card'),
        ('applepay', 'Apple Pay'),
    )

    STATUS_CHOICES = (
        ('initiated', 'Initiated'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('refunded', 'Refunded'),
        ('voided', 'Voided'),
        ('verified', 'Verified'),
    )

    payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default='SAR')
    description = models.TextField(blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id or 'Pending'} - {self.status}"
