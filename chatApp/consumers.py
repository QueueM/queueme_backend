import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoomModel, ChatHistoryModel
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender = data.get('sent_by')
        message = data.get('message')

        # Retrieve the chat room object (assumes room_name is the ID)
        chat_room = await sync_to_async(ChatRoomModel.objects.get)(id=self.room_name)
        await sync_to_async(ChatHistoryModel.objects.create)(
            room=chat_room,
            sent_by=sender,
            message=message
        )

        # Generate a bot reply via our AI chatbot feature.
        from ai_features import chatbot
        bot_reply = await sync_to_async(chatbot.get_response)(message, sender)
        await sync_to_async(ChatHistoryModel.objects.create)(
            room=chat_room,
            sent_by=3,
            message=bot_reply
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sent_by': sender,
                'message': message,
                'bot_reply': bot_reply
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sent_by': event['sent_by'],
            'message': event['message'],
            'bot_reply': event.get('bot_reply', '')
        }))
