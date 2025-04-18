from channels.generic.websocket import AsyncJsonWebsocketConsumer

class SalonFeatureConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = "salon_feature"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({"message": "Connected to Salon Feature updates."})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def salon_feature_update(self, event):
        data = event.get("data", {})
        await self.send_json(data)
