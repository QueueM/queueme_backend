from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    content_type = serializers.SlugRelatedField(
        slug_field='model',
        queryset=ContentType.objects.all()
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'title',
            'rating',
            'comment',
            'created_at',
            'content_type',
            'object_id',
            'sentiment_score'
        ]
        read_only_fields = ['id', 'created_at', 'sentiment_score']
