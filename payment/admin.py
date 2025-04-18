# File: payment/admin.py

from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "amount",
        "status",
        "payment_for",  # Updated to use the new field name
        "created_at",
    )
    fields = (
        "payment_id",
        "amount",
        "status",
        "payment_type",
        "payment_for",  # Updated field name
        "bill_name",
        "phone_number",
        "email",
        "address",
        "billing_cycle",
    )
    readonly_fields = ("created_at",)
    search_fields = ("payment_id", "status")
