# File: subscriptionApp/serializers.py

from rest_framework import serializers
from .models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel

class CompanySubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for subscription plan definitions.
    """
    class Meta:
        model = CompanySubscriptionPlansModel
        fields = ['id', 'name', 'price', 'duration_days', 'description']

# Backward-compatibility aliases
CompanySubscriptionPlansModelsSerializer = CompanySubscriptionPlanSerializer
CompanySubscriptionPlanModelSerializer = CompanySubscriptionPlanSerializer

class CompanySubscriptionDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for active company subscriptions.
    """
    plan = CompanySubscriptionPlanSerializer()

    class Meta:
        model = CompanySubscriptionDetailsModel
        fields = ['id', 'company', 'plan', 'billing_cycle', 'start_date', 'end_date']

# Backward-compatibility alias
CompanySubscriptionDetailsModelSerializer = CompanySubscriptionDetailsSerializer

class SubscriptionPaymentIntegrationRequestSerializer(serializers.Serializer):
    """
    Request payload for associating a payment with a subscription.
    """
    company = serializers.IntegerField()
    plan = serializers.IntegerField()
    billing_cycle = serializers.ChoiceField(choices=[('monthly','monthly'),('yearly','yearly')])
    payment_id = serializers.CharField()
    status = serializers.CharField()

class SubscriptionPaymentIntegrationResponseSerializer(serializers.Serializer):
    """
    Response after integrating a subscription payment.
    """
    message = serializers.CharField()
    plan = serializers.IntegerField()
    payment_id = serializers.CharField()
    status = serializers.CharField()

