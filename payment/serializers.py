# File: payment/serializers.py
from rest_framework import serializers

class PaymentCreateRequestSerializer(serializers.Serializer):
    payment_for = serializers.ChoiceField(choices=[('subscription','subscription'),('ads','ads'),('merchant','merchant')])
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    source = serializers.DictField(child=serializers.CharField(), required=False)
    metadata = serializers.DictField(child=serializers.CharField(), required=False)
    description = serializers.CharField(required=False, allow_blank=True)

class PaymentCreateResponseSerializer(serializers.Serializer):
    payment = serializers.DictField()
    payment_record_id = serializers.IntegerField()

class PaymentProcessingRequestSerializer(serializers.Serializer):
    payment_id = serializers.CharField()
    payment_for = serializers.ChoiceField(choices=[('subscription','subscription'),('ads','ads'),('merchant','merchant')])

class PaymentProcessingResponseSerializer(serializers.Serializer):
    payment_status = serializers.CharField()

class DemoPaymentResponseSerializer(serializers.Serializer):
    demo_payment = serializers.DictField()
    payment_record_id = serializers.IntegerField()

class WebhookMetadataSerializer(serializers.Serializer):
    payment_for = serializers.CharField()
    payment_type = serializers.CharField(required=False)
    bill_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    address = serializers.CharField(required=False)
    billing_cycle = serializers.CharField(required=False)

class WebhookDataSerializer(serializers.Serializer):
    id = serializers.CharField()
    status = serializers.CharField()
    amount = serializers.CharField()
    metadata = WebhookMetadataSerializer()

class WebhookRequestSerializer(serializers.Serializer):
    data = WebhookDataSerializer()

class WebhookResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    status = serializers.CharField()

