from rest_framework import serializers
from .models import CompanySubscriptionDetailsModel, CompanySubscriptionPlansModel
from .models import Payment
from django.utils import timezone

class CompanySubscriptionDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscriptionDetailsModel
        fields = "__all__"


class CompanySubscriptionPlansModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscriptionPlansModel
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    subscription_id = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Amount should be greater than 0")

        request = self.context.get('request')
        user = request.user
        company = user.company
        subscription_id = self.initial_data.get("subscription_id")

        if not subscription_id:
            raise serializers.ValidationError("Subscription ID is required")

        try:
            subscription_plan = CompanySubscriptionPlansModel.objects.get(pk=subscription_id)
        except CompanySubscriptionPlansModel.DoesNotExist:
            raise serializers.ValidationError("Subscription plan not found") 
        # Check if the company has a subscription
        company_subscription = CompanySubscriptionDetailsModel.objects.filter(company=company , end_date__gte=timezone.now() ).first()
        
        if company_subscription:
                required_amount = company_subscription.have_to_pay(new_plan_price=subscription_plan.price)
                if amount < required_amount:
                    raise serializers.ValidationError(
                        f"Amount should be at least {required_amount}"
                    )
        else:
            if amount != subscription_plan.price:
                raise serializers.ValidationError(
                    f"Amount should be exactly {subscription_plan.price}"
                )

        return amount
