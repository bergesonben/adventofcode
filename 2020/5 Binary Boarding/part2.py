from itertools import product
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

def getRowAndCol(boardingPass):
    return (getRow(boardingPass), getCol(boardingPass))

def hasFrontAndBackSeat(allSeats, seat):
    return (seat[0]+1, seat[1]) in allSeats and (seat[0]-1, seat[1]) in allSeats

def main(input):
    with open(input) as f:
        lines = f.readlines()

    allSeats = set()
    for line in lines:
        position = getRowAndCol(line)
        allSeats.add(position)

    allPossibleSeats = set(product(range(MAX_ROW+1), range(MAX_COL+1)))
    missingSeats = allPossibleSeats.difference(allSeats)
    mySeats = set()
    for missingSeat in missingSeats:
        if hasFrontAndBackSeat(allSeats, missingSeat):
            mySeats.add(missingSeat)
    if len(mySeats) != 1:
        print('oops')
    else:
        mySeat = mySeats.pop()
        print(mySeat[0]*8+mySeat[1])
    