

from rest_framework import serializers
from .models import CompanySubscriptionDetailsModel, CompanySubscriptionPlansModel


class CompanySubscriptionDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscriptionDetailsModel
        fields = "__all__"

class CompanySubscriptionPlansModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscriptionPlansModel
        fields = "__all__"