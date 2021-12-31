MAX_ROW = 127
MAX_COL = 7

def getPosition(boardingPass, maximum, upperLetter, lowerLetter, rangeToCheck):
    newRange = (0,maximum)
    for i in rangeToCheck:
        if boardingPass[i] == upperLetter:
            newRange = (newRange[0], ((newRange[1]+newRange[0]))//2)
        elif boardingPass[i] == lowerLetter:
            newRange = (((newRange[1]+newRange[0])+1)//2, newRange[1])
        else:
            raise Exception('Unexpect letter in boardingpass')
    if newRange[0] != newRange[1]:
        raise Exception('unexpected item in bagging area')
    return newRange[0]

def getRow(boardingPass):
    return getPosition(boardingPass, MAX_ROW, 'F', 'B', range(0,7))

def getCol(boardingPass):
    return getPosition(boardingPass, MAX_COL, 'L', 'R', range(7,10))

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
