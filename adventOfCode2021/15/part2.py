import sys

# DIRECTIONS = {'NORTH': (-1, 0), 'NORTHEAST': (-1, 1), 'EAST': (0, 1), 'SOUTHEAST': (1, 1), 'SOUTH': (1, 0), 'SOUTHWEST': (1, -1), 'WEST': (0, -1), 'NORTHWEST': (-1, -1)}
DIRECTIONS = {'NORTH': (-1, 0), 'EAST': (0, 1),'SOUTH': (1, 0),'WEST': (0, -1)}

def isInBound(row, col, max):
    return row >= 0 and row < max and col >= 0 and col < max

def getRiskValue(grid, row, col):
    limit = len(grid)
    ogValue = grid[row % limit][col % limit]
    adder = (row // limit) + (col // limit)
    newValue = (ogValue + adder) % 9
    newValue = 9 if newValue == 0 else newValue
    return newValue

def makeGrid():
    with open('input') as f:
        lines = f.readlines()  
    grid = []
    for line in lines:
        row = []
        for c in line.strip():
            row.append(int(c))
        grid.append(row)    
    return grid

def main(): 
    grid = makeGrid()
    end = (len(grid) * 5) -1 
    riskMap = {0:[(0,0)]}
    beenThere = set()
    beenThere.add((0,0))
    foundEnd = False
    answer = 0
    bestPath = set()
    bestPath.add((0,0))
    while not foundEnd:
        minValkey = min(riskMap.keys())
        minVals = riskMap[minValkey]
        # print(minValkey)
        # print(minVals)
        del riskMap[minValkey]
        for minVal in minVals:
            bestPath.add(minVal)
            for dir in DIRECTIONS.values():                
                newRow = minVal[0] + dir[0]
                newCol = minVal[1] + dir[1]
                if not isInBound(newRow, newCol, end + 1): continue
                if (newRow, newCol) in beenThere: continue
                newRiskVal = minValkey + getRiskValue(grid, newRow, newCol)
                if newRiskVal in riskMap:
                    riskMap[newRiskVal].append((newRow, newCol))
                else:
                    riskMap[newRiskVal] = [(newRow, newCol)]
                beenThere.add((newRow, newCol))
                if newRow == end and newCol == end:
                    foundEnd = True
                    answer = newRiskVal
    print(answer)
    # for i in range(end+1):
    #     toPrint = ''
    #     for j in range(end+1):
    #         toPrint += str(getRiskValue(grid, i, j))
    #     print(toPrint)


        

if __name__ == '__main__':
    sys.exit(main())

