# shopDashboardApp/consumers.py

from channels.generic.websocket import AsyncJsonWebsocketConsumer

class QueueDashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        params = self.scope["url_route"]["kwargs"]
        if "shop_id" in params:
            self.group_name = f"queue_dashboard_shop_{params['shop_id']}"
        elif "company_id" in params:
            self.group_name = f"queue_dashboard_company_{params['company_id']}"
        else:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def queue_update(self, event):
        await self.send_json(event["data"])
