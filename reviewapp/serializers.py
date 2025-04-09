# reviewapp/serializers.py
from rest_framework import serializers
from .models import Review
from django.contrib.contenttypes.models import ContentType

class ReviewSerializer(serializers.ModelSerializer):
    # Represent content_type as the model's name (e.g., "companysubscriptiondetailsmodel")
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
            # 'service',  # Uncomment if using the optional service field
        ]
        read_only_fields = ['id', 'created_at', 'sentiment_score']
