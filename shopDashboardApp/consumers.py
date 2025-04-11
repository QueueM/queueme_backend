# shopDashboardApp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class QueueDashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the URL parameters
        self.shop_id = self.scope['url_route']['kwargs'].get('shop_id')
        self.company_id = self.scope['url_route']['kwargs'].get('company_id')

        # Build the group name based on which parameter is provided
        if self.shop_id:
            self.group_name = f"dashboard_shop_{self.shop_id}"
        elif self.company_id:
            self.group_name = f"dashboard_company_{self.company_id}"
        else:
            self.group_name = "dashboard_general"

        # Join the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group upon disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # (Optional) Process incoming messages if needed
        try:
            data = json.loads(text_data)
            print("Received message:", data)
        except Exception as e:
            print("Error processing received data:", e)

    async def dashboard_update(self, event):
        """
        This method is called when a message of type 'dashboard_update' is sent to the group.
        It expects the event to have a 'data' key.
        """
        data = event.get("data", {})
        await self.send(text_data=json.dumps(data))
