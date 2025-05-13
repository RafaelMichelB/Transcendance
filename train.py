def calcIntersections(A1, A2, B1, B2) :
    x1, y1 = A1
    x2, y2 = A2
    x3, y3 = B1
    x4, y4 = B2

    dXSpeed = x2 - x1
    dYSpeed = y2 - y1

    dXWall = x4 - x3
    dYWall = y4 - y3

    originDiffX = x3 - x1
    originDiffY = y3 - y1
    determinant = dXSpeed * dYWall - dYSpeed * dXWall

    if abs(determinant) < 1e-3 :
        return None, None
    
    timePercent = (originDiffX * dYWall - originDiffY * dXWall) / determinant
    wallPercent = (originDiffX * dYSpeed - originDiffY * dXSpeed) / determinant

    #print(f"timePercent={timePercent}\nwallPercent={wallPercent}")

    if ( 0 <= timePercent <= 1 and 0 <= wallPercent <= 1 ) :
        return (timePercent, wallPercent)

    return (None, None)


calcIntersections((999.95, 350), (1000.400, 350), (1000, 300), (1000, 400))
