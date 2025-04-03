import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Group name
        self.room_group_name = 'game_stats'

        # Add the consumer to send him the API response
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # To do, is here to handle correctly the game actions
        pass

    async def send_game_stats(self, event):
        game_stats = event['game_stats']

        await self.send(text_data=json.dumps({
            'game_stats': game_stats
        }))

