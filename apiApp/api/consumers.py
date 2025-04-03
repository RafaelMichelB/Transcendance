import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "game_room"
        self.game_running = False
        self.task = None 

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("Connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        print(action)
        if action == "start":
            if not self.game_running:
                self.game_running = True
                self.task = asyncio.create_task(self.send_game_updates())
        elif action == "stop":
            self.game_running = False
            if self.task:
                self.task.cancel()
        elif action == "move":
            player1Move:str = data.get("player1")
            player2Move:str = data.get("player2")
            print(f"Player 1 move at {player1Move}, player 2 at {player2Move}")

    async def game_update(self, event):
        game_stats = event.get('game_stats', {})

        await self.send(text_data=json.dumps({
            'game_stats': game_stats
        }))
    
    async def send_game_updates(self) -> None:
        while self.game_running:
            await asyncio.sleep(1)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "game_update",
                    "game_stats": {
                        "score": 100,
                        "time": "00:01"
                    }
                }
            )

