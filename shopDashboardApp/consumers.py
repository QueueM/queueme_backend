import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.shop_id = self.scope['url_route']['kwargs'].get('shop_id')
        self.company_id = self.scope['url_route']['kwargs'].get('company_id')
        if self.shop_id:
            self.group_name = f"dashboard_shop_{self.shop_id}"
        elif self.company_id:
            self.group_name = f"dashboard_company_{self.company_id}"
        else:
            self.group_name = "dashboard_general"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def dashboard_update(self, event):
        data = event.get("data", {})
        await self.send(text_data=json.dumps(data))
