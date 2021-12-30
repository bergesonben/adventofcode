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
        
    def getListOfCoordinates(self):
        retval = []
        if self.isHorizontal:
            for i in range(min(self.start.y, self.end.y), max(self.start.y, self.end.y)+1):
                retval.append(Coordinate(self.start.x, i))
        elif self.isVertical:
            for i in range(min(self.start.x, self.end.x), max(self.start.x, self.end.x)+1):
                retval.append(Coordinate(i, self.start.y))
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
            if myRange.isHorizontal or myRange.isVertical:
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

