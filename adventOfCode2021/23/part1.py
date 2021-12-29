import sys
import copy

IS_TEST = True
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/23/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/23/input'

AMPHIPODS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

ROOMS = {
    'A': [(2,3), (3,3)],
    'B': [(2,5), (3,5)],
    'C': [(2,7), (3,7)],
    'D': [(2,9), (3,9)]
}

HALLWAY_SPOTS = {
    (1,1), (1,2), (1,4), (1,6), (1,8), (1,10), (1,11)
}

def inHallway(row):
    return row == 1

def inDeep(row):
    return row == 3

def isBlocked(row, col, layout):
    if layout[row-1][col] != '.':
        return True

def inRightRoom(a, row, col, layout):    
    if not a in ROOMS: 
        raise Exception("invalid a passed into inRightRoom")
    if (row, col) == ROOMS[a][1]:
        return True
    if (row, col) == ROOMS[a][0]:
        if layout[row+1][col] == a:
            return True    
    return False

def getPathCostOrNone(type, start, end, layout):
    numMoves = 0      
    if start[1] < end[1]: # going from left to right
        myRange = range(start[1], end[1]+1)
    else: #going from right to left
        myRange = range(end[1], start[1]+1)
    for col in myRange:
        if col == start[1]: 
            continue
        if layout[1][col] != '.':
            return None
        numMoves += 1  
    
    if end[0] > 1: #going from hallway to room
        myRange = range(start[0], end[0]+1)     
        col = end[1]   
    else: #going from room to hallway
        myRange = range(end[0], start[0]+1)
        col = start[1]
    for row in myRange:
        if row == start[0]:
            continue
        if layout[row][col] != '.':
            return None
        numMoves += 1
    return numMoves * AMPHIPODS[type]

def getValidHallwayMoveAndCost(row, col, layout):
    amphType = layout[row][col]
    room = ROOMS[amphType]
    roomDeepRow = room[1][0]
    roomDeepCol = room[1][1]
    inRoomType = layout[roomDeepRow][roomDeepCol]    
    if inRoomType != '.' and not inRightRoom(inRoomType, roomDeepRow, roomDeepCol, layout):
        return None        
    end = (roomDeepRow, roomDeepCol) if inRoomType == '.' else (roomDeepRow-1, roomDeepCol)
    cost = getPathCostOrNone(amphType, (row, col), end, layout)
    if cost is None:
        return None
    newLayout = copy.deepcopy(layout)
    newLayout[row][col] = '.'
    newLayout[end[0]][end[1]] = amphType
    return newLayout, cost

def getValidRoomMovesAndCosts(row, col, layout):
    amphType = layout[row][col]
    answers = []
    for spot in HALLWAY_SPOTS:
        cost = getPathCostOrNone(amphType, (row, col), spot, layout)
        if cost is None:
            continue
        newLayout = copy.deepcopy(layout)
        newLayout[row][col] = '.'
        newLayout[spot[0]][spot[1]] = amphType
        answers.append((copy.deepcopy(newLayout), cost))

    return answers

def printLayout(layout):
    for row in layout:
        line = ''
        for char in row:
            line += char
        print(line)       

def hashableLayout(layout):
    flatList = sum(layout, [])
    return tuple(flatList)

def solutionFound(layout):
    for type, coors in ROOMS.items():
        for coor in coors:
            if layout[coor[0]][coor[1]] != type: 
                return False
    return True

def getMinCost(layout, tried):
    if solutionFound(layout):
        return 0, [layout]

    hashedLayout = hashableLayout(layout)
    if hashedLayout in tried:
        return tried[hashedLayout] 

    minCost = float('inf')
    minMoves = []
    for rowNum, row in enumerate(layout):
        for colNum, cell in enumerate(row):
            if not cell in AMPHIPODS: # empty space or walls
                continue
            if inRightRoom(cell, rowNum, colNum, layout):
                continue
            if inDeep(rowNum) and isBlocked(rowNum, colNum, layout):
                continue                
            elif inHallway(rowNum):
                meh = getValidHallwayMoveAndCost(rowNum, colNum, layout)
                if meh is None:
                    continue
                newLayout, cost = meh
                newMinCost, newMinMoves = getMinCost(newLayout, tried)
                newMinCost += cost                                
                if newMinCost < minCost:          
                    tried[hashedLayout] = (newMinCost, newMinMoves)          
                    minCost = newMinCost     
                    newMinMoves.insert(0, newLayout)           
                    minMoves = newMinMoves
            else:
                for newLayout, cost in getValidRoomMovesAndCosts(rowNum, colNum, layout):
                    newMinCost, newMinMoves = getMinCost(newLayout, tried)
                    newMinCost += cost                    
                    if newMinCost < minCost:
                        tried[hashedLayout] = (newMinCost, newMinMoves)
                        minCost = newMinCost                
                        newMinMoves.insert(0, newLayout)           
                        minMoves = newMinMoves
    return minCost, minMoves


def main(): 
    global IS_TEST
    IS_TEST =  True if '-t' in sys.argv else False
    input = TEST_INPUT if IS_TEST else ACTUAL_INPUT

    with open(input) as f:
        lines = f.readlines()
    
    layout = []
    for line in lines:
        row = []
        for char in line.replace('\n', ''):
            row.append(char)
        layout.append(row)
    
    printLayout(layout)
    tried = {}
    answer, moves = getMinCost(layout, tried)
    print(answer)
    # for move in moves:
    #     printLayout(move)

if __name__ == '__main__':
    sys.exit(main())

