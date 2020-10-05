import json
from channels.generic.websocket import AsyncWebsocketConsumer


class MessagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"{self.scope['user'].username}", self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"{self.scope['user'].username}", self.channel_name
        )

    async def receive(self, text_data):
        await self.send(text_data=json.dumps(text_data))
