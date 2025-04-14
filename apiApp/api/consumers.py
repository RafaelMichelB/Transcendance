import json
from channels.generic.websocket import AsyncWebsocketConsumer
from serverPong.ball import Movement, BallData, calcIntersections
from serverPong.Racket import dictInfoRackets
from .tournamentChallenge import dictTournament, Tournament
from serverPong.Map import Map
import asyncio
from urllib.parse import parse_qs
import sys

def calcAllIntersections(walls, ptRacket1, ptRacket2) :
	for w in walls:
		if (calcIntersections(w[0], w[1], ptRacket1, ptRacket2) != (None, None)) :
			return True
	return False

		
class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		query_string = self.scope['query_string'].decode('utf-8')
		params = parse_qs(query_string)

		# Extraire le paramètre 'room' de la chaîne de requête
		self.room_group_name = params.get('room', [None])[0]

		if not self.room_group_name:
			await self.close()  # Fermer la connexion si aucun room n'est spécifié
			return

		self.game_running = False
		self.task = None
		self.map = Map() #None
		dictInfoRackets[self.room_group_name] = {"racket1" : [[0, 365], [0,395]], "racket2" : [[1000, 365], [1000, 395]]}
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
		print(type(text_data).__name__, file=sys.stderr)
		data = json.loads(text_data)
		print(type(data).__name__, file=sys.stderr)
		print(f"???---??? : {data}", file=sys.stderr)
		action = data.get("action")

		print(action, file=sys.stderr)
		if action == "start":
			mapString = data.get("map", "default.json")
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
				if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket1"][0][0], dictInfoRackets[self.room_group_name]["racket1"][0][1] + 5), Point(dictInfoRackets[self.room_group_name]["racket1"][1][0], dictInfoRackets[self.room_group_name]["racket1"][1][1] + 5)) == False) # Need to check if it hits a wall
					dictInfoRackets[self.room_group_name]["racket1"][0][1] += 5
					dictInfoRackets[self.room_group_name]["racket1"][1][1] += 5
			elif (player1Move == "down") :
				if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket1"][0][0], dictInfoRackets[self.room_group_name]["racket1"][0][1] - 5), Point(dictInfoRackets[self.room_group_name]["racket1"][1][0], dictInfoRackets[self.room_group_name]["racket1"][1][1] - 5)) == False) # Need to check if it hits a wall
					dictInfoRackets[self.room_group_name]["racket1"][0][1] -= 5
					dictInfoRackets[self.room_group_name]["racket1"][1][1] -= 5
			if (player2Move == "up") :
				if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket2"][0][0], dictInfoRackets[self.room_group_name]["racket2"][0][1] + 5), Point(dictInfoRackets[self.room_group_name]["racket2"][1][0], dictInfoRackets[self.room_group_name]["racket2"][1][1] + 5)) == False) # Need to check if it hits a wall
					dictInfoRackets[self.room_group_name]["racket2"][0][1] += 5
					dictInfoRackets[self.room_group_name]["racket2"][1][1] += 5
			elif (player2Move == "down") :
				if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket2"][0][0], dictInfoRackets[self.room_group_name]["racket2"][0][1] - 5), Point(dictInfoRackets[self.room_group_name]["racket2"][1][0], dictInfoRackets[self.room_group_name]["racket2"][1][1] - 5)) == False) # Need to check if it hits a wall
				dictInfoRackets[self.room_group_name]["racket2"][0][1] -= 5
				dictInfoRackets[self.room_group_name]["racket2"][1][1] -= 5

	async def tempReceived(self, event) :
		print(f"HELLO TEMP HERE {event}", file=sys.stderr)
		print(f"TempReceived!!! {event['text_data']}", file=sys.stderr)
		await self.receive(event["text_data"])
	
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
		try:
			self.gameSimulation = Movement(BallData(), self.room_group_name, map=self.map, plnb=2) # Change informations if game module
			t2 = asyncio.create_task(self.run_simulation())

			while self.game_running:
				await asyncio.sleep(0.2)
					
				try:
					stats = await self.gameSimulation.toDictionnary()
					await self.channel_layer.group_send(
						self.room_group_name,
						{
							"type": "game_update",
							"game_stats": stats,
						}
					)
				except Exception as e:
					print(f"!!! Failed to send update: {e}", file=sys.stderr)
		except asyncio.CancelledError:
			print("Task send_game_update Cancelled", file=sys.stderr)
			t2.cancel()
			await t2