from django.test import TestCase
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel
from .models import ChatRoomModel

class ChatAppTests(TestCase):
    def test_chat_room_str(self):
        user = User(username='testuser')
        # Assuming ShopDetailsModel has at least a name field.
        shop = ShopDetailsModel(name='Test Shop')
        room = ChatRoomModel(user=user, shop=shop)
        self.assertIn("ChatRoom", str(room))
