from rest_framework import serializers
from .models import ReelsModel, CommentsModel
from django.contrib.auth.models import User
from customersApp.models import CustomersDetailsModel
from usersapp.serializers import UserSerializer
from customersApp.models import CustomersDetailsModel
from customersApp.serializers import CustomersDetailsModelSerializer
from .models import StoryModel

class ReelSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.username')
    customer = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = ReelsModel
        fields = ['id', 'shop', 'video', 'caption', 'created_at', 'like_count', 'customer']

    def get_like_count(self, obj):
        return obj.like_count()
    
    def get_customer(self, obj):
        try:
            user = self.context['user']
            customer = user.customer  # Access related CustomerDetailsModel via related_name
            return CustomersDetailsModelSerializer(customer).data  # Serialize customer details
        except CustomersDetailsModel.DoesNotExist:
            return None  # Handle case where customer details do not exist

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    like_count = serializers.SerializerMethodField()
    liked_by = UserSerializer(many=True, read_only=True, source='likes')
    replies = serializers.SerializerMethodField()  # Include replies

    class Meta:
        model = CommentsModel
        fields = ['id', 'user', 'reel', 'text', 'created_at', 'like_count', 'liked_by', 'parent', 'replies']

    def get_like_count(self, obj):
        return obj.like_count()

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
            # return obj.replies.all()
        return []

class StorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = StoryModel
        fields = "__all__"