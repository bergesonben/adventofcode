import sys

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

    count = 0
    for key in lowPoints:
        count += lowPoints[key] + 1

    print(count)
    printHeightMap(lowPoints, heightMap)


    
    
if __name__ == '__main__':
    sys.exit(main())

