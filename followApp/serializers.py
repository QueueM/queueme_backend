# followApp/serializers.py
from rest_framework import serializers
from .models import ShopFollow
from shopApp.serializers import ShopDetailsModelSerializer
from shopApp.models import ShopDetailsModel

class ShopFollowSerializer(serializers.ModelSerializer):
    # full shop object on reads
    shop = ShopDetailsModelSerializer(read_only=True)
    # write‑only FK field for writes
    shop_id = serializers.PrimaryKeyRelatedField(
        queryset=ShopDetailsModel.objects.all(),
        write_only=True,
        source='shop'
    )

    class Meta:
        model = ShopFollow
        fields = ['id', 'shop', 'shop_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'shop']

    def create(self, validated_data):
        # attach customer automatically
        customer = self.context['request'].user.customersdetailsmodel
        validated_data['customer'] = customer
        return super().create(validated_data)

class FeedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content_type = serializers.CharField()
    created_at = serializers.DateTimeField()
    data = serializers.DictField()
