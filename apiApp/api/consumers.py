import json
from django.core.cache import cache
from channels.generic.websocket import AsyncWebsocketConsumer
from serverPong.ball import Movement, BallData, calcIntersections
from serverPong.Racket import dictInfoRackets
from .tournamentChallenge import dictTournament, Tournament
from serverPong.Map import Map
from serverPong.utilsClasses import Point, Vector
import asyncio
from urllib.parse import parse_qs
import sys
import random
import redis

def calcAllIntersections(walls, ptRacket1, ptRacket2) :
	for w in walls:
		# print(f"Actual wall : {w}", file=sys.stderr)	
		# print(f"wall : {w}\nptRacket: {ptRacket1} | {ptRacket2}\nResult calc intersections : {calcIntersections(w[0], w[1], ptRacket1, ptRacket2)}", file=sys.stderr)
		if (calcIntersections(w[0], w[1], ptRacket1, ptRacket2) != (None, None)) :
			print("Yep true", file=sys.stderr)
			return True
	return False


class GameConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		query_string = self.scope['query_string'].decode('utf-8')
		params = parse_qs(query_string)
		self.t2 = None

		# Extraire le paramètre 'room' de la chaîne de requête
		self.room_group_name = params.get('room', [None])[0]
		self.usrID = int(params.get('userid', [2])[0])
		print("room :", self.room_group_name, file=sys.stderr)
		print("user ID : ", self.usrID, file=sys.stderr)

		if not self.room_group_name:
			await self.close()
			return

		cache.set(f'simulation_state_{self.room_group_name}', {"State" : "Waiting for start"}, timeout=None)
		self.game_running = False
		self.task = None
		self.map = Map() #None
		dictInfoRackets[self.room_group_name] = {"racket1" : [[0, 300], [0,395]], "racket2" : [[1000, 300], [1000, 395]]}
		# print(dictInfoRackets, file=sys.stderr)

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()
		# print("Connected", file=sys.stderr)

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		# print("Disconnected", file=sys.stderr)


	async def receive(self, text_data):
		# print(type(text_data).__name__, file=sys.stderr)
		data = json.loads(text_data)
		print(f"Data: {data}",file=sys.stderr)
		# print(type(data).__name__, file=sys.stderr)
		# print(f"???---??? : {data}", file=sys.stderr)
		action = data.get("action")

		# print(action, file=sys.stderr)
		if action == "disconnect":
			print("yaay disconnection", file=sys.stderr)
			await self.disconnectUser(text_data)
        elif action == "forfait" :
            plId = data.get["player"]
            if plId == self.usrId :
                return dumps #<<<<----------------------------- REturn sdit'a win ou loose. 
		elif action == "start":
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
			try :
				player1Move:str = data.get("player1", "None")
				player2Move:str = data.get("player2", "None")
				# print(f"Player 1 move at {player1Move}, player 2 at {player2Move}", file=sys.stderr)
				if (player1Move == "down") :
					if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket1"][0][0], dictInfoRackets[self.room_group_name]["racket1"][0][1] + 5), Point(dictInfoRackets[self.room_group_name]["racket1"][1][0], dictInfoRackets[self.room_group_name]["racket1"][1][1] + 5)) == False) : # Need to check if it hits a wall
						dictInfoRackets[self.room_group_name]["racket1"][0][1] += 5
						dictInfoRackets[self.room_group_name]["racket1"][1][1] += 5
						# print(f"Down P1 {dictInfoRackets[self.room_group_name]['racket1']}", file=sys.stderr)
					else :
						print("Error 1", file=sys.stderr)
				elif (player1Move == "up") :
					if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket1"][0][0], dictInfoRackets[self.room_group_name]["racket1"][0][1] - 5), Point(dictInfoRackets[self.room_group_name]["racket1"][1][0], dictInfoRackets[self.room_group_name]["racket1"][1][1] - 5)) == False) : # Need to check if it hits a wall
						dictInfoRackets[self.room_group_name]["racket1"][0][1] -= 5
						dictInfoRackets[self.room_group_name]["racket1"][1][1] -= 5
						# print(f"UP P1 {dictInfoRackets[self.room_group_name]['racket1']}", file=sys.stderr)
					else :
						print("Error 2", file=sys.stderr)
				if (player2Move == "down") :
					if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket2"][0][0], dictInfoRackets[self.room_group_name]["racket2"][0][1] + 5), Point(dictInfoRackets[self.room_group_name]["racket2"][1][0], dictInfoRackets[self.room_group_name]["racket2"][1][1] + 5)) == False) : # Need to check if it hits a wall
						dictInfoRackets[self.room_group_name]["racket2"][0][1] += 5
						dictInfoRackets[self.room_group_name]["racket2"][1][1] += 5
						# print(f"Down P2 {dictInfoRackets[self.room_group_name]['racket2']}", file=sys.stderr)
					else :
						print("Error 3", file=sys.stderr)
				elif (player2Move == "up") :
					if (calcAllIntersections(self.map.walls, Point(dictInfoRackets[self.room_group_name]["racket2"][0][0], dictInfoRackets[self.room_group_name]["racket2"][0][1] - 5), Point(dictInfoRackets[self.room_group_name]["racket2"][1][0], dictInfoRackets[self.room_group_name]["racket2"][1][1] - 5)) == False) : # Need to check if it hits a wall
						dictInfoRackets[self.room_group_name]["racket2"][0][1] -= 5
						dictInfoRackets[self.room_group_name]["racket2"][1][1] -= 5
						# print(f"UP P2 {dictInfoRackets[self.room_group_name]['racket2']}", file=sys.stderr)
					else :
						print("Error 4", file=sys.stderr)
			except Exception as e :
				print(f"ERROR : {e}")

	async def tempReceived(self, event) :
		# print(f"HELLO TEMP HERE {event}", file=sys.stderr)
		# print(f"TempReceived!!! {event['text_data']}", file=sys.stderr)
		await self.receive(event["text_data"])

	async def disconnectUser(self, event) :
		if (self.usrID <= 1) :
			print("yikes", file=sys.stderr)
			await self.gameSimulation.stopSimulation()
		print("Disconnecteed from game !",file=sys.stderr)
		if self.t2 is not None :
			self.task.cancel()
			print("Yes t2 cancel", file=sys.stderr)
			await self.task
			cache.delete(f"simulation_state_{self.room_group_name}")
			await self.close()

	async def game_update(self, event):
		game_stats = event.get('game_stats', {})

		await self.send(text_data=json.dumps({
			'game_stats': game_stats
		}))
	
	async def run_simulation(self):
		try:
			# print("==> Inside run_simulation()", file=sys.stderr)
			await self.gameSimulation.doSimulation()
		except Exception as e:
			print(f"Simulation crashed: {e}", file=sys.stderr)

	async def send_game_updates(self) -> None:
		try:
			print("usrID send_game_update :", type(self.usrID).__name__, file=sys.stderr)
			if (self.usrID <= 1) :
				print("Yes !!!", file=sys.stderr)
				self.gameSimulation = Movement(BallData(), self.room_group_name, map=self.map, plnb=2, usrID=self.usrID) # Change informations if game module
				self.t2 = asyncio.create_task(self.run_simulation())

				while self.game_running:
					await asyncio.sleep(0.2)
					try:
						if self.usrID <= 1 :
							await self.gameSimulation.setRedisCache(self.room_group_name)
						r = redis.Redis(host='redis', port=6379, db=0)
						cles_redis = r.keys('*')
						print([clé.decode('utf-8') for clé in cles_redis], file=sys.stderr)
						stats = cache.get(f'simulation_state_{self.room_group_name}')
						print(f"caches: {str(cache)}", file=sys.stderr)
						# print(f"usrID : {self.usrID}\nstats: {stats}", file=sys.stderr)
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
			# print("Task send_game_update Cancelled", file=sys.stderr)
			self.t2.cancel()
			await self.t2

def checkCache() :
    r = redis.Redis(host='redis', port = 6379, db=0)
    cleRedis = r.keys('*')
    print([c.decode('utf-8') for c in cleRedis], file=sys.stderr)

