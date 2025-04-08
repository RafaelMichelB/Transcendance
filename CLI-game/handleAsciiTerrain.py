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


def getAsciiTerrain(map:Map, relation=20) :
    minX, maxX = map.borderX()
    minY, maxY = map.borderY()

    oneCharEquivalentX = round((maxX - minX) / relation)
    oneCharEquivalentY = round((maxY - minY) / relation)
    lstFinal = [[0 for i in range(oneCharEquivalentX + 1)] for i in range(oneCharEquivalentY + 1)]
    myWallsBordered = [[[round(i.x / relation), round(i.y / relation)] for i in k] for k in map.walls]
    # print(myWallsBordered)
    # print(lstFinal)
    # print(f"len : {len(lstFinal)}")
    for wall in myWallsBordered :
        listWall = calcYsement(wall[0], wall[1])
        for elem in listWall : 
            # print(f"wall: {wall}\nelem : {elem}")
            # print(f"dictionnaryWall[elem] : {dictionnaryWall[elem]}")
            lstFinal[elem[1]][elem[0]] = 1
    
    # print("---------------------------------------\n\n")
    # print(lstFinal)
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



ls = getAsciiTerrain(Map())
print(ls)
printState(ls, [600, 225])


    

