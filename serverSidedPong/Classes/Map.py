import math
import os
from utilsClasses import Vector, Point
import time
import numpy as np
import json

class Map() :
	''' Permit to create customs map, if we want to do the game customizaion option'''
	def __init__(self, filePath : str|None = None) :
		'''If no argument given or if the custom map has an error, it will generate default map'''
		if (filePath == None):
			self.walls : list[list[Point]] = [[Point(0, 0), Point(1000, 0)], [Point(0, 600), Point(1000, 600)], [Point(0, 0), Point(0, 150)], [Point(0, 450), Point(0, 600)], [Point(1000, 0), Point(1000, 150)], [Point(1000, 450), Point(1000, 600)]]
		else :
			with open(filePath) as jsonMap :
				listWalls : list[list[list[int]]] = json.load(jsonMap)
			tmpListWalls : list[list[Point]] = []
			isFine : bool = True
			for wall in listWalls :
				if len(wall) != 2 or len(wall[0]) != 2 or len(wall[1]) != 2:
					self.walls : list[list[Point]] = [[Point(0, 0), Point(1000, 0)], [Point(0, 600), Point(1000, 600)], [Point(0, 0), Point(0, 150)], [Point(0, 450), Point(0, 600)], [Point(1000, 0), Point(1000, 150)], [Point(1000, 450), Point(1000, 600)]] # Invalid map throw the default map
					isFine = False
					break
				else :
					tmpListWalls.append([Point(wall[0][0], wall[0][1]), Point(wall[1][0], wall[1][1])])
			if (isFine) :
				self.walls = tmpListWalls


# myMap1 = Map()

# print("--------------------- map1 ---------------------")
# listm1 = myMap1.walls
# for elem in listm1:
# 	print(str(elem), end=" ")
# print()


# myMap2 = Map("map.json")

# print("--------------------- map2 ---------------------")
# listm1 = myMap2.walls
# for elem in listm1:
# 	print(str(elem), end=" ")
# print()
