import sys
import copy

IS_TEST = True
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/23/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/23/input'
STEPS = []
STEPS_I = 0


AMPHIPODS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

ROOMS = {
    'A': [(2,3), (3,3), (4,3), (5,3)],
    'B': [(2,5), (3,5), (4,5), (5,5)],
    'C': [(2,7), (3,7), (4,7), (5,7)],
    'D': [(2,9), (3,9), (4,9), (5,9)]
}

HALLWAY_SPOTS = {
    (1,1), (1,2), (1,4), (1,6), (1,8), (1,10), (1,11)
}

def inHallway(row):
    return row == 1

def inDeep(row):
    return row > 2

def isBlocked(row, col, layout):
    for i in range(2, row):
        if layout[i][col] != '.':
            return True
    return False

def inRightRoom(a, row, col, layout):    
    if not a in ROOMS: 
        raise Exception("invalid a passed into inRightRoom")
    if (row, col) == ROOMS[a][3]:
        return True    
    elif (row, col) == ROOMS[a][2]:
        if layout[row+1][col] == a:
            return True
    elif (row, col) == ROOMS[a][1]:
        if layout[row+1][col] == a and layout[row+2][col] == a:
            return True
    elif (row, col) == ROOMS[a][0]:
        if layout[row+1][col] == a and layout[row+2][col] == a and layout[row+3][col] == a:
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
    for roomDeepRow, roomDeepCol in room:
        inRoomType = layout[roomDeepRow][roomDeepCol]    
        if inRoomType == '.':
            deepest = (roomDeepRow, roomDeepCol)
        elif not inRightRoom(inRoomType, roomDeepRow, roomDeepCol, layout):
            return None        
    cost = getPathCostOrNone(amphType, (row, col), deepest, layout)
    if cost is None:
        return None
    newLayout = copy.deepcopy(layout)
    newLayout[row][col] = '.'
    newLayout[deepest[0]][deepest[1]] = amphType
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
        return 0

    hashedLayout = hashableLayout(layout)

    # global STEPS_I
    # if hashedLayout == STEPS[STEPS_I]:
    #     print('reached step ' + str(STEPS_I))        
    #     STEPS_I += 1

    if hashedLayout in tried:
        return tried[hashedLayout] 

    # printLayout(layout)                  
    minCost = float('inf')
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
                newMinCost = getMinCost(newLayout, tried)
                newMinCost += cost                                
                if newMinCost < minCost:                              
                    minCost = newMinCost                     
            else:
                meh = getValidRoomMovesAndCosts(rowNum, colNum, layout)
                for newLayout, cost in meh:
                    newMinCost = getMinCost(newLayout, tried)
                    newMinCost += cost                    
                    if newMinCost < minCost:
                        minCost = newMinCost                          
    tried[hashedLayout] = minCost
    return minCost

def setSteps():
    with open('/home/benjamin/Documents/adventOfCode2021/23/steps') as f:
        lines = f.readlines()
    
    layout = []
    for line in lines:
        if line.isspace():
            global STEPS
            STEPS.append(hashableLayout(layout))
            layout = []
        row = []
        for char in line.replace('\n', ''):
            row.append(char)
        layout.append(row)    

def main(): 
    global IS_TEST, STEPS
    IS_TEST =  True if '-t' in sys.argv else False
    input = TEST_INPUT if IS_TEST else ACTUAL_INPUT
    # setSteps()

    with open(input) as f:
        lines = f.readlines()    
    
    layout = []
    for line in lines:
        row = []
        for char in line.replace('\n', ''):
            row.append(char)
        layout.append(row)
    
    tried = {}
    answer = getMinCost(layout, tried)
    print(answer)

if __name__ == '__main__':
    sys.exit(main())

