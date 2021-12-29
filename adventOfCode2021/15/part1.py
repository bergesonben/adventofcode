import sys

# DIRECTIONS = {'NORTH': (-1, 0), 'NORTHEAST': (-1, 1), 'EAST': (0, 1), 'SOUTHEAST': (1, 1), 'SOUTH': (1, 0), 'SOUTHWEST': (1, -1), 'WEST': (0, -1), 'NORTHWEST': (-1, -1)}
DIRECTIONS = {'NORTH': (-1, 0), 'EAST': (0, 1),'SOUTH': (1, 0),'WEST': (0, -1)}

def isInBound(row, col, max):
    return row >= 0 and row < max and col >= 0 and col < max

def main(): 
    with open('input') as f:
        lines = f.readlines()  
    end = len(lines) - 1
    grid = []
    riskMap = {0:[(0,0)]}
    beenThere = set()
    beenThere.add((0,0))
    for line in lines:
        row = []
        for c in line.strip():
            row.append(int(c))
        grid.append(row)
    
    foundEnd = False
    answer = 0
    while not foundEnd:
        minValkey = min(riskMap.keys())
        minVals = riskMap[minValkey]
        # print(minValkey)
        # print(minVals)
        del riskMap[minValkey]
        for minVal in minVals:
            for dir in DIRECTIONS.values():                
                newRow = minVal[0] + dir[0]
                newCol = minVal[1] + dir[1]
                if not isInBound(newRow, newCol, end + 1): continue
                if (newRow, newCol) in beenThere: continue
                newRiskVal = minValkey + grid[newRow][newCol]
                if newRiskVal in riskMap:
                    riskMap[newRiskVal].append((newRow, newCol))
                else:
                    riskMap[newRiskVal] = [(newRow, newCol)]
                beenThere.add((newRow, newCol))
                if newRow == end and newCol == end:
                    foundEnd = True
                    answer = newRiskVal
    print(answer)


        

if __name__ == '__main__':
    sys.exit(main())

