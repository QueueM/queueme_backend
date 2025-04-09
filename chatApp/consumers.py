# chatApp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoomModel, ChatHistoryModel

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

        # Retrieve the chat room object using the room name (assumed to be the ChatRoomModel id)
        chat_room = await sync_to_async(ChatRoomModel.objects.get)(id=self.room_name)
        # Create the user chat message
        await sync_to_async(ChatHistoryModel.objects.create)(
            room=chat_room,
            sent_by=sender,
            message=message
        )

        # Generate bot reply using your AI chatbot feature.
        # If chatbot.get_response is synchronous, wrap it with sync_to_async.
        from ai_features import chatbot
        bot_reply = await sync_to_async(chatbot.get_response)(message, sender)

        # Save the bot reply as a separate chat history entry (assuming sent_by=3 for bot)
        await sync_to_async(ChatHistoryModel.objects.create)(
            room=chat_room,
            sent_by=3,
            message=bot_reply
        )

        # Broadcast both the user's message and bot reply to all members of the room.
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
        try:
            await self.send(text_data=json.dumps({
                'sent_by': event['sent_by'],
                'message': event['message'],
                'bot_reply': event.get('bot_reply', '')
            }))
        except Exception as e:
            # Log the exception; you might choose to add additional handling here.
            print("Error sending message over WebSocket:", e)
