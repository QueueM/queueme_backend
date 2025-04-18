# File: shopDashboardApp/serializers.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from .models import DashboardLog

class DashboardLogSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    branch_name  = serializers.CharField(source='shop.shop_name', default='', read_only=True)
    total_comments_per_reel = serializers.SerializerMethodField()

    class Meta:
        model = DashboardLog
        fields = [
            'id', 'timestamp', 'company', 'company_name', 'shop', 'branch_name',
            'total_bookings', 'total_revenue', 'total_specialists',
            'total_waiting', 'total_in_progress', 'total_completed', 'total_cancelled',
            'estimated_wait_time', 'total_employees', 'average_salary',
            'total_customers', 'customer_retention_rate', 'average_rating',
            'total_reels_likes', 'total_ad_impressions', 'total_ad_viewers', 'total_ad_clicks',
            'total_stories', 'total_story_likes', 'total_reels', 'total_comments_per_reel',
            'top_services'
        ]
        read_only_fields = fields

    @extend_schema_field(OpenApiTypes.INT)
    def get_total_comments_per_reel(self, obj):
        try:
            return int(obj.total_comments_per_reel)
        except (ValueError, TypeError):
            return 0
