import math
import os
from .utilsClasses import Vector, Point
import time
import numpy as np
from .Map import Map

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

	mat = np.array([
		[x2 - x1, -(x4 - x3)],
		[y2 - y1, -(y4 - y3)]
	])
	vec = np.array([x3 - x1, y3 - y1])

	det = np.linalg.det(mat)

	if abs(det) < 1e-10:
		return None, None

	u, v = np.linalg.solve(mat, vec)

	if 0 <= u <= 1 and 0 <= v <= 1:
		interX = x1 + u * (x2 - x1)
		interY = y1 + u * (y2 - y_1)
		return Point(interX, interY), v

	return None, None

def	normalizeNormalVector(vector:Vector) :
	norm = math.sqrt(vector.x**2 + vector.y**2)
	return Vector(round(vector.x / norm, 2), round(vector.y / norm, 2))

def calcDotProduct(vec1:Vector, vec2:Vector) :
	return vec1.x * vec2.x + vec1.y * vec2.y
	
class	BallData() :
	def __init__(self, position:Point=Point(0, 0), speed:Vector=Vector(1, 0)) : # Are 0,0 the center of the game ? 
		self.pos:Point = position
		self.spd:Vector = speed
	
	def __str__(self) -> str :
		return (f"Position of ball is : {self.position}\nMovement vector is {self.spd}")

	def getData(self) -> dict :
		return ({"position" : [self.pos], "speed" : [self.spd]})
	def calculateReflexionVector(self, wallHit:Vector) -> Vector :
		normalVector = normalizeNormalVector(wallHit)
		return Vector(self.spd.x - 2 * calcDotProduct(self.spd, normalVector) * normalVector.x, self.spd.y - 2 * calcDotProduct(self.spd, normalVector) * normalVector.y) le 
		

class	Movement() :
	def __init__(self, ballInfo : BallData, map:Map=Map(), timestamp:float = time.time()) :
		self.running : bool = True
		self.ball : BallData = ballInfo
		self.racket1 : RacketData | None = None
		self.racket2 : RacketData | None = None
		self.ts : float = timestamp
		self.map : Map = myMap

	async def calculateLinearMovement(self, vectorMovement : Vector, time : float) -> Point :
		return (Point(self.ball.pos.x + vectorMovement.x * time, self.ball.pos.y + vectorMovement.y * time))

	async def isWallIntersection(self, pointTrajectory: Point, timeLeft : float) -> float:
		minTimeWallHit : float = 2.0
		intersectionPoint = Point(100000, 100000)
		allWals = self.map + self.racket1.positions + self.racket2.positions
		wallHit:list | None = None
		for wall in allWalls:
			valueIntersections = calcIntersections(wall[0], wall[1], self.ball.pos, pointTrajectory)
			if valueIntersections[1] != None and valueIntersections[1] < timeLeft and valueIntersections[1] < minTimeWallHit:
				minTimeWallHit = valueIntersections[1]
				intersectionPoint = valueIntersections[0]
				wallHit = wall
		if (minTimeWallHit != 2.0) :
			self.ball.position = intersectionPoint
			self.ball.spd = self.ball.calculateReflexionVector(Vector(wallHit[0], wallHit[1]))
			return (timeLeft - minTimeWallHit)
		else :
			self.ball.pos = pointTrajectory
			return (0.0)
		
	async def getWallsHit(self) -> None :
		timeLeft : float = 0.005
		while timeLeft > 0.0:
			linearMovementPoint:Point = self.calculateLinearMovement(self.ball.spd, timeLeft)
			timeLeft = self.isWallIntersection(linearMovementPoint, timeLeft)
	
	async def toDictionnary(self) -> dict :
		return ({"player1" : self.racket1.getData(), "player2" : self.racket2.getData(), "ball" : self.ball.getData()})
	async def doSimulation(self) :
		iteration = 0
		while running:
			self.racket1 = dictInfo.get("racket1", Racket())
			self.racket2 = dictInfo.get("racket2", Racket())
			self.getWallsHit()
			iteration += 1
			if iteration % 10 == 0: #50 ms
				pass #need to establish how to send data to client
			if iteration % 200 == 0: # 1000ms , 1 second
				pass #need to establish how to send data to AI
	def stopSimultation(self) :
		self.running = False

	


# Formula linear movement : 
# 	xNew = xOld + vectorX * deltaT
# 	yNew = yOld + vectorY * deltaT

# Formula Reflection :
# 	normalizedNormalVector = normalVector / norm
# 	newVec = oldVec - 2 * (oldVec . normalizedNormalVector) * normalizedNormalVector


		
