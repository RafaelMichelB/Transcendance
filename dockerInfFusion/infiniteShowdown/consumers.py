import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Tu peux gérer la déconnexion ici si besoin

    async def receive(self, text_data):
        # Pour un simple écho
        await self.send(text_data=json.dumps({
            'message': text_data
        }))

