
from customClasses.BaseFilterSet import BaseFilterSet
from .models import ReelsModel, CommentsModel

class ReelsFilter(BaseFilterSet):
    class Meta:
        model = ReelsModel
        fields = '__all__'
        
class ReelsCommentsFilter(BaseFilterSet):
    class Meta:
        model = CommentsModel
        fields = '__all__'