import math
import os
from .utilsClasses import Vector, Point
import time
import numpy as np
from .Map import Map
import sys
from .Racket import dictInfoRackets

import asyncio

def convertToJsonList(elem) :
	return [[elem[0].x, elem[0].y], [elem[1].x, elem[1].y]]

def calcIntersections(A1 : Point, A2 : Point, B1 : Point, B2 : Point):
	"""
	Check Intersection beetween [A1 , A2] and [B1 , B2]

		if (ret1, ret2) == (None, None) -> No intersections
		else -> ret1 = Intersections point | ret2 = fraction of 1 sec (deadtime)
	"""

	x1, y1 = A1.toTuple()
	x2, y2 = A2.toTuple()
	x3, y3 = B1.toTuple()
	x4, y4 = B2.toTuple()

	dXSpeed = x2 - x1
	dYSpeed = y2 - y1

	dXWall = x4 - x3
	dYWall = y4 - y3

	originDiffX = x3 - x1
	originDiffY = y3 - y1
	determinant = dXSpeed * dYWall - dYSpeed * dXWall

	file = open("output.txt", 'a')

	if abs(determinant) < 1e-3 :
		return None, None
	
	timePercent = (originDiffX * dYWall - originDiffY * dXWall) / determinant
	wallPercent = (originDiffX * dYSpeed - originDiffY * dXSpeed) / determinant

	file.write(f"----------------------------------------------------------------\nWall:[[{x3}, {y3}], [{x4}, {y4}]]\nMovement:[[{x1}, {y1}], [{x2}, {y2}]]\ntimePercent={timePercent}\nwallPercent={wallPercent}\n")

	if ( 0 <= timePercent <= 1 and 0 <= wallPercent <= 1 ) :
		interX = x3 + wallPercent * (x4 - x3)
		interY = y3 + wallPercent * (y4 - y3)
		print(f"Yiikes: {Point(interX, interY)}", file=sys.stderr)
		return (Point(interX, interY), timePercent)

	return (None, None)

def	normalizeNormalVector(vector:Vector) :
	norm = math.sqrt(vector.x**2 + vector.y**2)
	return Vector(-(round(vector.y / norm, 2)), round(vector.x / norm, 2))

def calcDotProduct(vec1:Vector, vec2:Vector) :
	return vec1.x * vec2.x + vec1.y * vec2.y
	
class	BallData() :
	def __init__(self, position:Point=Point(500, 350), speed:Vector=Vector(90, 0)) : # Are 500,300 the center of the game ? 
		self.pos:Point = position
		self.spd:Vector = speed
	
	def __str__(self) -> str :
		return (f"Position of ball is : {self.position}\nMovement vector is {self.spd}")

	def getData(self) -> dict :
		return ({"position" : self.pos.toList(), "speed" : self.spd.toList()})
	def calculateReflexionVector(self, wallHit:Vector) -> Vector :
		normalVector = normalizeNormalVector(wallHit)
		print(f"NormalizedVector : {normalVector}", file=sys.stderr)
		print(f"Vector Reflected : {Vector(self.spd.x - 2 * calcDotProduct(self.spd, normalVector) * normalVector.x, self.spd.y - 2 * calcDotProduct(self.spd, normalVector) * normalVector.y)}", file=sys.stderr)
		return Vector(self.spd.x - 2 * calcDotProduct(self.spd, normalVector) * normalVector.x, self.spd.y - 2 * calcDotProduct(self.spd, normalVector) * normalVector.y)
		

class	Movement() :
	def __init__(self, ballInfo: BallData, map: Map = Map(), timestamp: float = time.time(), plnb: int = 2):
		try:
			# print("runningGame", file=sys.stderr)
			self.runningGame: bool = True
			# print("ball", file=sys.stderr)
			self.ball: BallData = ballInfo
			# print("racketlist", file=sys.stderr)
			self.racketList: list | None = None
			# print("nbplayers", file=sys.stderr)
			self.nbPlayers = plnb
			# print("ts", file=sys.stderr)
			self.ts: float = timestamp
			# print("map", file=sys.stderr)
			self.map: Map = map
		except Exception as e:
			print(f"Error in __init__: {e}", file=sys.stderr)

	async def calculateLinearMovement(self, vectorMovement : Vector, time : float) -> Point :
		return (Point(self.ball.pos.x + vectorMovement.x * time, self.ball.pos.y + vectorMovement.y * time))

	async def isWallIntersection(self, pointTrajectory: Point, timeLeft : float) -> float:
		# print(f"--> isWallIntersection() start")
		fileNone = open("outputNone.txt", 'a')
		minTimeWallHit : float = 2.0
		# print(f"--> isWallIntersection() minTimeWallHit={minTimeWallHit}")
		intersectionPoint = Point(100000, 100000)
		# print(f"--> isWallIntersection() intersectionPoint={intersectionPoint}")
		allWalls = self.map.walls + self.racketList
		# print(f"--> isWallIntersection() allWalls={allWalls}")
		wallHit:list | None = None
		# print(f"--> isWallIntersection() wallHit={wallHit}")
		for wall in allWalls:
			# print(f"--> isWallIntersection() wall={wall}")
			valueIntersections = calcIntersections(wall[0], wall[1], self.ball.pos, pointTrajectory)
			fileNone.write(f"--> isWallIntersection() valueIntersection={valueIntersections}\n")
			# --> isWallIntersection() valueIntersection=(< 1000.0, 350.0 >, 0.5)
			if valueIntersections[1] != None and valueIntersections[1] < minTimeWallHit:
				minTimeWallHit = valueIntersections[1] * timeLeft
				print(f"--> isWallIntersection() GET minTimeWallHit={minTimeWallHit}", file=sys.stderr)
				intersectionPoint = valueIntersections[0]
				# print(f"--> isWallIntersection() GET intersectionPoint={intersectionPoint}")
				wallHit = wall
				# print(f"--> isWallIntersection() GET wallHit={wallHit}")
		fileNone.close()
		if (minTimeWallHit != 2.0) :
			# print(f"--> isWallIntersection() YEP minTimeWallHit={minTimeWallHit}")
			self.ball.position = intersectionPoint
			# print(f"--> isWallIntersection() YEP self.ball.position={self.ball.position}")
			self.ball.spd = self.ball.calculateReflexionVector(Vector(wallHit[0], wallHit[1]))
			print(f"--> isWallIntersection() YEP self.ball.speed={self.ball.spd}", file=sys.stderr)
			return (timeLeft - minTimeWallHit)
		else :
			self.ball.pos = pointTrajectory
			return (0.0)
		
	async def getWallsHit(self) -> None :
		# print("-> getWallsHit() start")
		timeLeft : float = 0.005
		# print("-> getWallsHit() timeLetf set")

		# print("-> getWallsHit() start while")
		while timeLeft > 0.0:
			# print(f"-> getWallsHit() timeleft={timeLeft}")
			linearMovementPoint:Point = await self.calculateLinearMovement(self.ball.spd, timeLeft)
			# print(f"-> getWallsHit() linearMovementPoint={linearMovementPoint}")
			# print("----------------------------------------------------------------")
			timeLeft = await self.isWallIntersection(linearMovementPoint, timeLeft)
			# print(f"-> getWallsHit() afterIteration : timeleft={timeLeft}")
	
	async def toDictionnary(self) -> dict :
		ditctionnaryPlayers = dict((f'player{i}', convertToJsonList(self.racketList[i])) for i in range(len(self.racketList)))
		ditctionnaryPlayers["ball"] = self.ball.getData()
		return (ditctionnaryPlayers)

	async def doSimulation(self) :
		# print(">>> Entered doSimulation()", file=sys.stderr)
		iteration = 0
		while self.runningGame:
			# print(f">>> Iteration {iteration}", file=sys.stderr)
			self.racketList = []
			for i in range(1, self.nbPlayers + 1):
				# print(f">>> Getting racket data for racket{i}", file=sys.stderr)
				try :
					self.racketList.append([Point(dictInfoRackets[f"racket{i}"][0][0], dictInfoRackets[f"racket{i}"][0][1]), Point(dictInfoRackets[f"racket{i}"][1][0], dictInfoRackets[f"racket{i}"][1][1])])
				except Exception as e:
					print(f"!!! Error building racketList: {e}", file=sys.stderr)
			# print(self.racketList)
			await self.getWallsHit()
			iteration += 1
			await asyncio.sleep(0.005)

	async def stopSimultation(self) :
		self.runningGame = False

	


# Formula linear movement : 
# 	xNew = xOld + vectorX * deltaT
# 	yNew = yOld + vectorY * deltaT

# Formula Reflection :
# 	normalizedNormalVector = normalVector / norm
# 	newVec = oldVec - 2 * (oldVec . normalizedNormalVector) * normalizedNormalVector


		
