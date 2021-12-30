import sys
class Coordinate:
    def __init__(self, x, y):
            self.x = int(x)
            self.y = int(y)

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.isHorizontal = self.start.x == self.end.x
        self.isVertical = self.start.y == self.end.y
        self.is45Degrees = abs(self.start.x-self.end.x) == abs(self.start.y-self.end.y)
        # print(str(self) + ' is45Degrees: ' + str(self.is45Degrees))
        
    def getListOfCoordinates(self):
        retval = []
        if self.isHorizontal:
            for i in range(min(self.start.y, self.end.y), max(self.start.y, self.end.y)+1):
                retval.append(Coordinate(self.start.x, i))
        elif self.isVertical:
            for i in range(min(self.start.x, self.end.x), max(self.start.x, self.end.x)+1):
                retval.append(Coordinate(i, self.start.y))
        elif self.is45Degrees:
            xDirection = -1 if self.start.x - self.end.x > 0 else 1
            yDirection = -1 if self.start.y - self.end.y > 0 else 1
            xList = [*range(self.start.x, self.end.x + xDirection, xDirection)]
            yList = [*range(self.start.y, self.end.y + yDirection, yDirection)]
            # print(str(self) + ' xList = ' + str(xList) + '; yList = ' + str(yList))
            for x,y in zip(xList, yList):
                retval.append(Coordinate(x, y))
        else:
            raise Exception('getListOfCoordinates called on range that is not vertical or horizontal')
        
        return retval

    def __str__(self):
        return str(self.start) + ' -> ' + str(self.end)


class Board:
    def __init__(self, ranges):
        self.ranges = ranges
        self.board = {}

        for myRange in ranges:
            if myRange.isHorizontal or myRange.isVertical or myRange.is45Degrees:
                coorList = myRange.getListOfCoordinates()
                for coor in coorList:
                    if (coor.x, coor.y) in self.board:
                        self.board[coor.x, coor.y] += 1
                    else:
                        self.board[(coor.x, coor.y)] = 1

def parseRanges():
    with open('input') as f:
        lines = f.readlines()
        ranges = []
        for line in lines:
            rawCoors = line.split(' -> ')
            rawStart = rawCoors[0].split(',')
            start = Coordinate(int(rawStart[0]), int(rawStart[1]))
            rawEnd = rawCoors[1].split(',')
            end = Coordinate(int(rawEnd[0]), int(rawEnd[1]))
            ranges.append(Range(start, end))
    return ranges

def main(): 
    ranges = parseRanges()
    board = Board(ranges)
    count = 0
    for coor in board.board:
        if board.board[coor] > 1:
            count += 1
    print(count)
    
    
if __name__ == '__main__':
    sys.exit(main())

