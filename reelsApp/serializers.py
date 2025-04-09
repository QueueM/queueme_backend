# reelsApp/serializers.py
from rest_framework import serializers
from .models import ReelsModel, CommentsModel, StoryModel
from django.contrib.auth.models import User
from customersApp.serializers import CustomersDetailsModelSerializer
from usersapp.serializers import UserSerializer
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer

class ReelSerializer(CustomBaseModelSerializer):
    customer = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = ReelsModel
        fields = ['id', 'shop', 'video', 'caption', 'created_at', 'like_count', 'customer', 'ai_video_tags']

    def get_like_count(self, obj):
        return obj.like_count()
    
    def get_customer(self, obj):
        try:
            user = self.context['user']
            customer = user.customer
            return CustomersDetailsModelSerializer(customer).data
        except Exception:
            return None

class CommentSerializer(CustomBaseModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    like_count = serializers.SerializerMethodField()
    liked_by = UserSerializer(many=True, read_only=True, source='likes')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = CommentsModel
        fields = ['id', 'user', 'reel', 'text', 'created_at', 'like_count', 'liked_by', 'parent', 'replies']

    def get_like_count(self, obj):
        return obj.like_count()

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class StorySerializer(CustomBaseModelSerializer):
    class Meta:
        model = StoryModel
        fields = '__all__'
