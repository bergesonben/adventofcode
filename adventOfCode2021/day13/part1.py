import sys
from enum import Enum

class Direction(Enum):
    X = 'x'
    Y = 'y'

X = 0
Y = 1

def initiate():
    with open('/home/benjamin/Documents/adventOfCode2021/day13/input') as f:
        lines = f.readlines()   
    
    foundFolds = False
    coordinates = set()
    folds = []
    maxX = 0
    maxY = 0
    for line in lines:
        if line.isspace():
            foundFolds = True 
            continue
        if foundFolds:
            folds.append(Fold(line))
        else:
            parsed = line.split(',')
            x = int(parsed[X].strip())
            y = int(parsed[Y].strip())
            maxX = max(maxX, x)
            maxY = max(maxY, y)
            coordinates.add((x,y))
    return coordinates, folds, maxX, maxY

class Fold:
    def __init__(self, raw):
        parsed = raw.split(' ')
        self.direction = Direction.Y if parsed[2][0] == 'y' else Direction.X
        self.value = int(parsed[2].split('=')[1])

    def __str__(self):
        return 'fold along ' + str(self.direction) + '=' + str(self.value)

class Paper:
    def __init__(self):
        self.coordinates, self.folds, self.maxX, self.maxY = initiate()

    def makeAllTheFolds(self):
        for i in range(len(self.folds)):
            self.makeFold()

    def makeFold(self):
        newSet = set()
        fold = self.folds.pop(0)
        max = self.maxX if fold.direction == Direction.X else self.maxY
        if fold.value >= max // 2:
            for coor in self.coordinates:
                if fold.direction == Direction.X:
                    self.maxX = fold.value-1
                    if coor[X] > fold.value:                        
                        newSet.add((2 * fold.value - coor[X], coor[Y]))
                    else:
                        newSet.add(coor)
                else:
                    self.maxY = fold.value-1
                    if coor[Y] > fold.value:
                        newSet.add((coor[X], 2 * fold.value - coor[Y]))
                    else:
                        newSet.add(coor)
        else:
            print('well shit')

        self.coordinates = newSet

    def printPaper(self):
        # zeros = [ [0]*M for _ in range(N) ]
        temp = [['.']*(self.maxX+1) for _ in range(self.maxY+1)]
        for coor in self.coordinates:
            temp[coor[Y]][coor[X]] = '#'
        for row in temp:
            toPrint = ''
            for val in row:
                toPrint += val
            print(toPrint)


def main(): 
    paper = Paper()
    paper.makeAllTheFolds()
    paper.printPaper()
    
    

    
if __name__ == '__main__':
    sys.exit(main())

