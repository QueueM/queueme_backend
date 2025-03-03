
from customClasses.BaseFilterSet import BaseFilterSet
from .models import ReelsModel, CommentsModel, StoryModel

class ReelsFilter(BaseFilterSet):
    class Meta:
        model = ReelsModel
        fields = '__all__'
        
class ReelsCommentsFilter(BaseFilterSet):
    class Meta:
        model = CommentsModel
        fields = '__all__'

class StoryFilter(BaseFilterSet):
    class Meta:
        model = StoryModel
        fields = '__all__'