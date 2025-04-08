import json
from channels.generic.websocket import AsyncWebsocketConsumer
from serverPong.ball import Movement, BallData
from serverPong.Racket import dictInfoRackets
from .tournamentChallenge import dictTournament, Tournament
import asyncio
import sys

class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = "game_room"
		self.game_running = False
		self.task = None
		dictInfoRackets[self.room_group_name] = {"racket1" : [[0, 300], [0,400]], "racket2" : [[1000, 300], [1000,400]]}
		print(dictInfoRackets, file=sys.stderr)

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
		print("Connected", file=sys.stderr)

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		print("Disconnected", file=sys.stderr)

	async def receive(self, text_data):
		data = json.loads(text_data)
		action = data.get("action")

		print(action, file=sys.stderr)
		if action == "start":
			# INTEGRATE MAP CHECKER 
			if not self.game_running:
				self.game_running = True
				self.task = asyncio.create_task(self.send_game_updates())
		elif action == "stop":
			self.game_running = False
			if self.task:
				self.task.cancel()
		elif action == "move":
			player1Move:str = data.get("player1", "None")
			player2Move:str = data.get("player2", "None")
			print(f"Player 1 move at {player1Move}, player 2 at {player2Move}", file=sys.stderr)
			if (player1Move == "up") :
				# if () # Need to check if it hits a wall
				dictInfoRackets[self.room_group_name]["racket1"][0][1] += 5
				dictInfoRackets[self.room_group_name]["racket1"][1][1] += 5
			elif (player1Move == "down") :
				# if () # Need to check if it hits a wall
				dictInfoRackets[self.room_group_name]["racket1"][0][1] -= 5
				dictInfoRackets[self.room_group_name]["racket1"][1][1] -= 5
			if (player2Move == "up") :
				# if () # Need to check if it hits a wall
				dictInfoRackets[self.room_group_name]["racket2"][0][1] += 5
				dictInfoRackets[self.room_group_name]["racket2"][1][1] += 5
			elif (player2Move == "down") :
				# if () # Need to check if it hits a wall
				dictInfoRackets[self.room_group_name]["racket2"][0][1] -= 5
				dictInfoRackets[self.room_group_name]["racket2"][1][1] -= 5


				


	async def game_update(self, event):
		game_stats = event.get('game_stats', {})

		await self.send(text_data=json.dumps({
			'game_stats': game_stats
		}))
	
	async def run_simulation(self):
		try:
			print("==> Inside run_simulation()", file=sys.stderr)
			await self.gameSimulation.doSimulation()
		except Exception as e:
			print(f"Simulation crashed: {e}", file=sys.stderr)

	async def send_game_updates(self) -> None:
		# print("==> Starting simulation setup...", file=sys.stderr)
		try:
			self.gameSimulation = Movement(BallData(), self.room_group_name, plnb=2) # Change informations if game module
			# print("==> Movement object created", file=sys.stderr)
			t2 = asyncio.create_task(self.run_simulation())
			# print("==> Simulation task launched", file=sys.stderr)

			# print(f"==> game_running = {self.game_running}", file=sys.stderr)
			while self.game_running:
				# print("==> Tick", file=sys.stderr)
				await asyncio.sleep(0.2)
				# print("==> After sleep", file=sys.stderr)
					
				try:
					stats = await self.gameSimulation.toDictionnary()
					await self.channel_layer.group_send(
						self.room_group_name,
						{
							"type": "game_update",
							"game_stats": stats,
						}
					)
				# print("==> Stats sent", file=sys.stderr)
				except Exception as e:
					print(f"!!! Failed to send update: {e}", file=sys.stderr)
		except asyncio.CancelledError:
			print("Task send_game_update Cancelled")
			t2.cancel()
			await t2