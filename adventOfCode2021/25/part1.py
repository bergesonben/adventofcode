import sys
import copy

IS_TEST = True
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/25/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/25/input'

EAST = '>'
SOUTH = 'v'
EMPTY = '.'

class SeaFloor():
    def __init__(self, lines):
        self.value = []        
        for line in lines:
            row = []
            for c in line.strip():
                row.append(c)    
            self.value.append(row)
        self.width = len(self.value[0])
        self.height = len(self.value)

    def hashable(self):
        retval = ''
        for row in self.value:
            for c in row:
                retval += c
        return retval
    
    def eastOneSpot(self, colIndex):
        return colIndex + 1 if colIndex < self.width-1 else 0

    def southOneSpot(self, rowIndex):
        return rowIndex + 1 if rowIndex < self.height-1 else 0

    def isEastEmpty(self, rowIndex, colIndex):
        eastOneSpot = self.eastOneSpot(colIndex)
        return self.value[rowIndex][eastOneSpot] == EMPTY

    def isSouthEmpty(self, rowIndex, colIndex):
        southOneSpot = self.southOneSpot(rowIndex)
        return self.value[southOneSpot][colIndex] == EMPTY

    def moveEastRow(self, rowIndex):
        newRow = []
        skipNext = False
        for colIndex, spot in enumerate(self.value[rowIndex]):
            if skipNext: 
                skipNext = False
                continue
            if spot == EMPTY or spot == SOUTH:
                newRow.append(spot)
            elif self.isEastEmpty(rowIndex, colIndex):
                newRow.append(EMPTY)
                if colIndex == self.width-1:
                    newRow[0] = EAST
                else:
                    newRow.append(EAST)
                skipNext = True
            else:
                newRow.append(spot)
        self.value[rowIndex] = newRow

    def moveSouthColumn(self, colIndex):
        newCol = []
        skipNext = False
        for rowIndex in range(self.height):
            spot = self.value[rowIndex][colIndex]
            if skipNext: 
                skipNext = False
                continue
            if spot == EMPTY or spot == EAST:
                newCol.append(spot)
            elif self.isSouthEmpty(rowIndex, colIndex):
                newCol.append(EMPTY)
                if rowIndex == self.height-1:
                    newCol[0] = SOUTH
                else:
                    newCol.append(SOUTH)
                skipNext = True
            else:
                newCol.append(spot)
            
        for otherRowIndex in range(self.height):
            self.value[otherRowIndex][colIndex] = newCol[otherRowIndex]


    def moveEastHerd(self):
        for rowIndex in range(0, self.height):
            self.moveEastRow(rowIndex)
    
    def moveSouthHerd(self):
        for colIndex in range(0, self.width):
            self.moveSouthColumn(colIndex)

    def move(self):
        self.moveEastHerd()
        self.moveSouthHerd()

    def __str__(self):
        string = ''
        for row in self.value:
            for c in row:
                string += c
            string += '\n'
        return string[:-1]

def main(): 
    global IS_TEST
    if not '-t' in sys.argv:
        IS_TEST = False
    INPUT = TEST_INPUT if IS_TEST else ACTUAL_INPUT    
    with open(INPUT) as f:
        lines = f.readlines()

    seaFloor = SeaFloor(lines)
    prevValue = ''
    currValue = seaFloor.hashable()
    numMoves = 0   
    while prevValue != currValue:
        seaFloor.move()
        prevValue = currValue
        currValue = seaFloor.hashable()
        numMoves += 1
    print(numMoves)

if __name__ == '__main__':
    sys.exit(main())

