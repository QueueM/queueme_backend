import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ReelsModel

class ReelsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.reel_id = self.scope['url_route']['kwargs']['reel_id']
        self.group_name = f"reel_{self.reel_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Example: broadcast a simple update
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'reel_update',
                'data': data
            }
        )

    async def reel_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
