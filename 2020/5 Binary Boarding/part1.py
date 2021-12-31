MAX_ROW = 127
MAX_COL = 7

def getRow(boardingPass):
    newRange = (0,MAX_ROW)
    for i in range(0,7):
        if boardingPass[i] == 'F':
            newRange = (newRange[0], ((newRange[1]+newRange[0]))//2)
        elif boardingPass[i] == 'B':
            newRange = (((newRange[1]+newRange[0])+1)//2, newRange[1])
        else:
            raise Exception('Unexpect letter in boardingpass')
    if newRange[0] != newRange[1]:
        raise Exception('you done fucked up getting the row')
    return newRange[0]

def getCol(boardingPass):
    newRange = (0,MAX_COL)
    for i in range(7,10):
        if boardingPass[i] == 'L':
            newRange = (newRange[0], (newRange[1]+newRange[0])//2)
        elif boardingPass[i] == 'R':
            newRange = (((newRange[1]+newRange[0])+1)//2, newRange[1])
        else:
            raise Exception('Unexpect letter in boardingpass')
    if newRange[0] != newRange[1]:
        raise Exception('you done fucked up getting the column')
    return newRange[0]

def getSeatId(boardingPass):
    row = getRow(boardingPass)
    col = getCol(boardingPass)

    return row * 8 + col

def main(input):
    with open(input) as f:
        lines = f.readlines()

    maxSeatId = float('-inf')
    for line in lines:
        seatId = getSeatId(line)
        maxSeatId = max(seatId, maxSeatId)
    print(maxSeatId)
