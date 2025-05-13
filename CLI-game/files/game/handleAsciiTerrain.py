import math
import os
import time
import json
import curses
# from files.createMatch import sendLobby

class Point() :
    '''Point classes, permit an easier work on the calc, with overload operator'''
    def __init__(self, xPoint : float, yPoint : float) :
        '''
            init a Point class with x and y
        '''
        self.x: float = xPoint
        self.y: float = yPoint

    def __str__(self) -> str :
        '''
            Return a string interpretation for the point, for better reading
        '''
        return (f"Point is : ({self.x}, {self.y})")

    def __repr__(self) -> str :
        '''
            Return a list containing x and y of point, to better data construction on JSON creations functions.
        '''
        return (f"< {self.x}, {self.y} >")

    ''' Comparisons operator : == and != '''
    def __eq__(self, other : 'Point') -> bool :
        if (isinstance(other, Point) == False) :
            return False
        elif (self.x != other.x or self.y != other.y) :
            return False
        return True

    def __ne__(self, other : 'Point') -> bool :
        if (isinstance(other, Point) == False) :
            return False
        elif (self.x != other.x or self.y != other.y) :
            return True
        return False

    ''' Arithmetic operator : 
        + -> (1 + 2 = 3)
        - -> (10 - 2 = 8)
        * -> (3 * 2 = 6)
        / -> (3 / 2 = 1.5)
        ** -> (3 ** 2 = 9)
        // -> (5 // 3 = 1)
        % -> (5 % 3 = 2)
    '''
    def __add__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x + other.x, self.y + other.y))
    
    def __sub__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x - other.x, self.y - other.y))
    
    def __mul__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else  :
            return (Point(self.x * other.x, self.y * other.y))

    def __truediv__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x / other.x, self.y / other.y))
    
    def __floordiv__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x // other.x, self.y // other.y))
    
    def __mod__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x % other.x, self.y % other.y))
    
    def __pow__(self, other : 'Point') -> 'Point' :
        if (isinstance(other, Point) == False) :
            return Point(-1, -1)
        else :
            return (Point(self.x ** other.x, self.y ** other.y))

    ''' Assignement operators :
        -=
        +=
        *=
        /=
        //=
        %=
        **=
    '''
    def __isub__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x -= other.x
        self.y -= other.y
    
    def __iadd__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x += other.x
        self.y += other.y
    
    def __imul__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x *= other.x
        self.y *= other.y

    def __idiv__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x /= other.x
        self.y /= other.y
    
    def __ifloordiv__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x //= other.x
        self.y //= other.y
    
    def __imod__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x %= other.x
        self.y %= other.y

    def __ipow__(self, other : 'Point') -> None :
        if (isinstance(other, Point) == False) :
            return  
        self.x **= other.x
        self.y **= other.y

    def toTuple(self) -> tuple :
        return ((self.x, self.y))
    def toList(self) -> list :
        return ([self.x, self.y])

class Map() :
    ''' Permit to create customs map, if we want to do the game customizaion option'''
    def __init__(self, filePath : str|None = None) :
        '''If no argument given or if the custom map has an error, it will generate default map'''
        self.center = Point(500, 300)
        if (filePath == None):
            self.walls : list[list[Point]] = [[Point(-5, 0), Point(1005, 0)], [Point(-5, 600), Point(1005, 600)]]
            self.winningTeam1 = [Point(-5, -50), Point(-5, 650)]
            self.winningTeam2 = [Point(1005, -50), Point(1005, 650)]
        else :
            with open(filePath) as jsonMap :
                dictParsingMap = json.load(jsonMap)
            listWalls = dictParsingMap["Walls"]
            tmpListWalls : list[list[Point]] = []
            isFine : bool = True
            for wall in listWalls :
                if len(wall) != 2 or len(wall[0]) != 2 or len(wall[1]) != 2:
                    self.walls : list[list[Point]] = [[Point(0, 0), Point(1000, 0)], [Point(0, 600), Point(1000, 600)], [Point(0, 0), Point(0, 150)], [Point(0, 450), Point(0, 600)], [Point(1000, 0), Point(1000, 150)], [Point(1000, 450), Point(1000, 600)]] # Invalid map throw the default map
                    isFine = False
                    break
                else :
                    tmpListWalls.append([Point(wall[0][0], wall[0][1]), Point(wall[1][0], wall[1][1])])
            winningT1 = dictParsingMap.get("WinningTeam1", [])
            winningT2 = dictParsingMap.get("WinningTeam2", [])
            if (isFine) :
                self.walls = tmpListWalls
            else : 
                self.walls = [[Point(0, 0), Point(1000, 0)], [Point(0, 600), Point(1000, 600)], [Point(0, 0), Point(0, 150)], [Point(0, 450), Point(0, 600)], [Point(1000, 0), Point(1000, 150)], [Point(1000, 450), Point(1000, 600)]]
            if (winningT1 != []) :
                self.winningTeam1 = [Point(winningT1[0][0], winningT1[0][1]), Point(winningT1[1][0], winningT1[1][1])]
            else :
                self.winningTeam1 = [Point(-5, 0), Point(-5, 600)]
            if (winningT2 != []) :
                self.winningTeam2 = [Point(winningT2[0][0], winningT2[0][1]), Point(winningT2[1][0], winningT2[1][1])]
            else :
                self.winningTeam2 = [Point(1005, 0), Point(1005, 600)]

    def borderX(self) :
        minX = 99999999
        maxX = -99999999
        for elements in self.walls :
            if (elements[0].x < minX) :
                minX = elements[0].x
            if (elements[0].x > maxX) :
                maxX = elements[0].x
            if (elements[1].x < minX) :
                minX = elements[1].x
            if (elements[1].x > maxX) :
                maxX = elements[1].x
        return (minX, maxX)

    def borderY(self) :
        minY = 99999999
        maxY = -99999999
        for elements in self.walls :
            if (elements[0].y < minY) :
                minY = elements[0].y
            if (elements[0].y > maxY) :
                maxY = elements[0].y
            if (elements[1].y < minY) :
                minY = elements[1].y
            if (elements[1].y > maxY) :
                maxY = elements[1].y
        return (minY, maxY)


def calcYsement(A, B):
    x1, y1 = A
    x2, y2 = B
    if (x1 == x2) :
        return [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)]

    
    m = (y2 - y1) / (x2 - x1)
    
    b = y1 - m * x1
    
    resultats = []

    for x in range(x1, x2 + 1):
        y = m * x + b
        resultats.append((x, round(y)))
    
    return resultats


def getAsciiTerrain(map:Map, rcktDict, relation=30) :
    minX, maxX = map.borderX()
    minY, maxY = map.borderY()
    oneCharEquivalentX = round((maxX - minX) / relation)
    oneCharEquivalentY = round((maxY - minY) / relation)
    valuepl1 = rcktDict["game_stats"]["player1"]
    valuepl2 = rcktDict["game_stats"]["player2"]

    lstFinal = [[0 for i in range(oneCharEquivalentX + 1)] for j in range(oneCharEquivalentY + 1)]
    myWallsBordered = [[[round(i.x / relation), round(i.y / relation)] for i in k] for k in map.walls] + [[[round(valuepl1[0][0] / relation), round(valuepl1[0][1] / relation)], [round(valuepl1[1][0] / relation), round(valuepl1[1][1] / relation)]], [[round(valuepl2[0][0] / relation), round(valuepl2[0][1] / relation)], [round(valuepl2[1][0] / relation), round(valuepl2[1][1] / relation)]]]
    ##print(myWallsBordered)
    for wall in myWallsBordered :
        listWall = calcYsement(wall[0], wall[1])
        for elem in listWall : 
            try :
                lstFinal[elem[1]][elem[0]] = 1
            except Exception as e :
                pass
    
    return lstFinal


def printState(mapList, ballCoo, relation=30) :
    ascciBallPos = [round(ballCoo[0] / relation), round(ballCoo[1] / relation)]
    toReturn = ""
    for subList in range(len(mapList)) :
        for elem in range(len(mapList[subList])) :
            if [elem, subList] == ascciBallPos : 
                toPrint = 'o '
            elif mapList[subList][elem] == 1 :
                toPrint = 'XX'
            else :
                toPrint = '  '
            toReturn += toPrint
        toReturn += "\n"
    return toReturn

def mainPrinter(racketDictionnary, stdscr, key=None, map=Map()) :
    ls = getAsciiTerrain(map, racketDictionnary)
    return printState(ls, racketDictionnary['game_stats']['ball']['position'])


        # return (racketDictionnary["finalScore"], stdscr, key)

# racketDictionnary = {
    # "game_stats": {
        # "player1": 
            # [[0, 250], [0, 350]],
        # "player2": 
        # [[1000, 250], [1000, 350]], 
        # "ball": {
            # "position": 
                # [500, 425], 
            # "speed": 
                # [90, 0]
                # }, 
        # "team1Score": 0,
        # "team2Score": 0
        # }
    # }
# mainPrinter(
# ls = getAsciiTerrain(Map(), racketDictionnary)

# #print(printState(ls, [600, 225]))


    

