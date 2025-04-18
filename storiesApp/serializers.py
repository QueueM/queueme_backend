from rest_framework import serializers
from customClasses.CustomBaseModelSerializer import CustomBaseModelSerializer
from .models import StoryModel, StoryViewedModel

class StorySerializer(CustomBaseModelSerializer):
    view_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = StoryModel
        fields = '__all__'

class StoryViewedSerializer(CustomBaseModelSerializer):
    class Meta:
        model = StoryViewedModel
        fields = '__all__'
