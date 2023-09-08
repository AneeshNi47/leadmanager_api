import json
from channels.generic.websocket import AsyncWebsocketConsumer

class LeadsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("leads", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("leads", self.channel_name)

    async def new_lead(self, event):
        await self.send(text_data=json.dumps(event))

    async def deleted_lead(self, event):
        await self.send(text_data=json.dumps(event))
