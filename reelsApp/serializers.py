# File: reelsApp/serializers.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import ReelsModel, CommentsModel

class ReelSerializer(CustomBaseModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = ReelsModel
        fields = [
            'id', 'shop', 'video', 'caption', 'thumbnail', 'created_at',
            'like_count', 'view_count', 'share_count', 'save_count',
            'ai_video_tags', 'processed_video_url', 'analytics_data'
        ]

    @extend_schema_field(OpenApiTypes.INT)
    def get_like_count(self, obj):
        return obj.like_count()

class CommentSerializer(CustomBaseModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    like_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = CommentsModel
        fields = ['id', 'user', 'reel', 'text', 'created_at', 'like_count', 'parent', 'replies']

    @extend_schema_field(OpenApiTypes.INT)
    def get_like_count(self, obj):
        return obj.like_count()

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_replies(self, obj):
        """
        Return nested list of reply comments.
        """
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data if qs.exists() else []
