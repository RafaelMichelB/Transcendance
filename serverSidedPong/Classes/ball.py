import math
import os
from .utilsClasses import Vector, Point

class	BallData() :
	def __init__(self, position:Point=Point(0, 0), speed:Vector=Vector(1, 0)) : # Are 0,0 the center of the game ? 
		self.pos:Point = position
		self.spd:Vector = speed
	
	def __str__(self) -> str :
		return (f"Position of ball is : {self.position}\nMovement vector is {self.spd}")

	def __repr__(self) -> dict :
		return ({"position" : [self.pos], "speed" : [self.spd]})


class	BallMovement() :
	def __init__(self) :
		vector : Vect
        