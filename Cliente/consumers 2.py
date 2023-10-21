from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BasicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Por enquanto, vamos apenas ecoar a mesma mensagem de volta.
        await self.send(text_data=text_data)