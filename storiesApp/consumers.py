import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StoriesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.story_id = self.scope['url_route']['kwargs']['story_id']
        self.group_name = f"story_{self.story_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'story_update',
                'data': data
            }
        )

    async def story_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
