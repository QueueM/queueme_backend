



from rest_framework import serializers

from .models import CustomersDetailsModel



class CustomersDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomersDetailsModel
        fields = "__all__"