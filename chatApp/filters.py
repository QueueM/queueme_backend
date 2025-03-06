



from customClasses.BaseFilterSet import BaseFilterSet
from .models import ChatRoomModel, ChatHistoryModel

class ChatRoomFilter(BaseFilterSet):

    class Meta:
        model = ChatRoomModel
        fields = '__all__'

class ChatHistoryFilter(BaseFilterSet):

    class Meta:
        model = ChatHistoryModel
        fields = '__all__'