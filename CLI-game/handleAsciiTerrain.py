from apiApp.serverPong.Map import Map

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


def getAsciiTerrain(map:Map, rcktDict, relation=20) :
    minX, maxX = map.borderX()
    minY, maxY = map.borderY()

    oneCharEquivalentX = round((maxX - minX) / relation)
    oneCharEquivalentY = round((maxY - minY) / relation)
    valuepl1 = rcktDict["game_stats"]["player1"]
    valuepl2 = rcktDict["game_stats"]["player2"]

    lstFinal = [[0 for i in range(oneCharEquivalentX + 1)] for i in range(oneCharEquivalentY + 1)]
    myWallsBordered = [[[round(i.x / relation), round(i.y / relation)] for i in k] for k in map.walls] + [[[round(valuepl1[0][0] / relation), round(valuepl1[0][1] / relation)], [round(valuepl1[1][0] / relation), round(valuepl1[1][1] / relation)]], [[round(valuepl2[0][0] / relation), round(valuepl2[0][1] / relation)], [round(valuepl2[1][0] / relation), round(valuepl2[1][1] / relation)]]]
    print(myWallsBordered)
    for wall in myWallsBordered :
        listWall = calcYsement(wall[0], wall[1])
        for elem in listWall : 
            lstFinal[elem[1]][elem[0]] = 1
    
    return lstFinal

def printState(mapList, ballCoo, relation=20) :
    ascciBallPos = [round(ballCoo[0] / relation), round(ballCoo[1] / relation)]
    for subList in range(len(mapList)) :
        for elem in range(len(mapList[subList])) :
            if [elem, subList] == ascciBallPos : 
                toPrint = 'o'
            elif mapList[subList][elem] == 1 :
                toPrint = 'X'
            else :
                toPrint = ' '
            print(toPrint, end='')
        print()



racketDictionnary = {
    "game_stats": {
        "player1": 
            [[0, 250], [0, 350]],
        "player2": 
            [[1000, 250], [1000, 350]], 
        "ball": {
            "position": 
                [500, 425], 
            "speed": 
                [90, 0]
                }, 
        "team1Score": 0,
        "team2Score": 0
        }
    }

ls = getAsciiTerrain(Map(), racketDictionnary)

printState(ls, [600, 225])


    

