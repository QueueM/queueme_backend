"""
subscriptionApp/serializers.py

Serializers for subscription models.
Includes validation logic for payments.
"""

from rest_framework import serializers
from .models import CompanySubscriptionDetailsModel, CompanySubscriptionPlansModel, Payment
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from django.utils import timezone

class CompanySubscriptionDetailsModelSerializer(CustomBaseModelSerializer):
    """
    Serializer for CompanySubscriptionDetailsModel.
    """
    class Meta:
        model = CompanySubscriptionDetailsModel
        fields = "__all__"


class CompanySubscriptionPlansModelsSerializer(CustomBaseModelSerializer):
    """
    Serializer for CompanySubscriptionPlansModel.
    """
    class Meta:
        model = CompanySubscriptionPlansModel
        fields = "__all__"


class PaymentSerializer(CustomBaseModelSerializer):
    """
    Serializer for Payment model.
    Adds a read-only subscription_id field.
    """
    subscription_id = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    def validate_amount(self, amount):
        """
        Validates that the amount is greater than 0 and matches the expected price for the plan.
        """
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise serializers.ValidationError("Invalid amount format.")

        if amount <= 0:
            raise serializers.ValidationError("Amount should be greater than 0.")

        request = self.context.get("request")
        user = request.user
        company = user.company
        subscription_id = self.initial_data.get("subscription_id")
        billing_cycle = self.initial_data.get("billing_cycle", "monthly")

        if not subscription_id:
            raise serializers.ValidationError("Subscription ID is required.")

        try:
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
        except CompanySubscriptionPlansModel.DoesNotExist:
            raise serializers.ValidationError("Subscription plan not found.")

        if billing_cycle == "yearly":
            if not subscription_plan.yearly_price:
                raise serializers.ValidationError("Yearly price is not set for this plan.")
            required_amount = subscription_plan.yearly_price
        else:
            required_amount = subscription_plan.price

        if round(amount, 2) != round(float(required_amount), 2):
            raise serializers.ValidationError(
                f"Amount should be exactly {required_amount} for {billing_cycle} billing."
            )

        return amount
