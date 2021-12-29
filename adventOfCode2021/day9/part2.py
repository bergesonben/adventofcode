import sys

debug = False

def hasLowerNeighbors(row, column, heightMap):
    val = heightMap[row][column]
    if row > 0 and heightMap[row-1][column] <= val: # check up
        return True
    elif row < len(heightMap)-1  and heightMap[row+1][column] <= val: # check down
        return True
    elif column > 0 and heightMap[row][column-1] <= val: # check left
        return True
    elif column < len(heightMap[0])-1  and heightMap[row][column+1] <= val: # check right
        return True
    else:
        return False  

def printHeightMap(lowPoints, heightMap):
    for rowIndex, row in enumerate(heightMap):
        toPrint = ''
        for colIndex, val in enumerate(row):
            if (rowIndex, colIndex) in lowPoints:
                toPrint += '\033[92m' + str(val) + '\033[0m'
            else:
                toPrint += str(val)
        print(toPrint)

def printVisitedMap(visitedMap, heightMap):
    for rowIndex, row in enumerate(heightMap):
        toPrint = ''
        for colIndex, val in enumerate(row):
            if visitedMap[rowIndex][colIndex]:
                toPrint += '\033[92m' + str(val) + '\033[0m'
            else:
                toPrint += str(val)
        print(toPrint)

def isDirectionInbound(rowIndex, colIndex, rowMax, colMax):    
    if rowIndex >= 0 and rowIndex <= rowMax and colIndex >= 0 and colIndex <= colMax:
        if debug: print('isDirectionInbound(' + str(rowIndex) + ', ' + str(colIndex) + ', ' + str(rowMax) + ', ' + str(colMax) + '): True')
        return True
    else:
        if debug: print('isDirectionInbound(' + str(rowIndex) + ', ' + str(colIndex) + ', ' + str(rowMax) + ', ' + str(colMax) + '): False')
        return False

def getBasinSize(rowIndex, colIndex, val, heightMap, visitedMap):
    if debug: print('getBasizeSize(' + str(rowIndex) + ', ' + str(colIndex) + ', ' + str(val) + ')')   
    visitedMap[rowIndex][colIndex] = True
    if debug: printVisitedMap(visitedMap, heightMap)

    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)] # up, left, down, right
    size = 1
    for rowDirection, colDirection in DIRECTIONS:
        newRow = rowIndex + rowDirection
        newCol = colIndex + colDirection
        if isDirectionInbound(newRow, newCol, len(heightMap)-1, len(heightMap[0])-1) and heightMap[newRow][newCol] != 9 and visitedMap[newRow][newCol] == False:                        
            size += getBasinSize(newRow, newCol, heightMap[newRow][newCol], heightMap, visitedMap)
    
    return size

def getBasinSizes(lowPoints, heightMap):
    visitedMap = []
    for i, row in enumerate(heightMap):
        newRow = []
        for j, val in enumerate(row):
            newRow.append(False)
        visitedMap.append(newRow)    
    retval = []
    for key in lowPoints:
        retval.append(getBasinSize(key[0], key[1], lowPoints[key], heightMap, visitedMap))
    printVisitedMap(visitedMap, heightMap)
    
    return retval

def main(): 
    with open('input') as f:
        lines = f.readlines()
        
    heightMap = []
    for line in lines:
        row = [int(num) for num in line.strip()]
        heightMap.append(row)

    lowPoints = {}
    for rowIndex, row in enumerate(heightMap):
        for colIndex, val in enumerate(row):
            if not hasLowerNeighbors(rowIndex, colIndex, heightMap):
                lowPoints[(rowIndex, colIndex)] = val


    basinSizes = getBasinSizes(lowPoints, heightMap)
    basinSizes = list(reversed(sorted(basinSizes)))
    # print(basinSizes)
    print(basinSizes[0]*basinSizes[1]*basinSizes[2])
    


    
    
if __name__ == '__main__':
    sys.exit(main())

