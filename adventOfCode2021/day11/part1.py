import sys

DIRECTIONS = {'NORTH': (-1, 0), 'NORTHEAST': (-1, 1), 'EAST': (0, 1), 'SOUTHEAST': (1, 1), 'SOUTH': (1, 0), 'SOUTHWEST': (1, -1), 'WEST': (0, -1), 'NORTHWEST': (-1, -1)}

class Octopus:
    def __init__(self, level):
        self.level = level
        self.isFlashing = False

    def __str__(self):
        if self.isFlashing:
            return  '\033[92m' + str(self.level) + '\033[0m'
        else:
            return str(self.level)

    def increaseOrNone(self):
        if self.isFlashing: return None
        elif self.level == 9:
            self.isFlashing = True
            self.level = 0
            return True
        else:
            self.level += 1
        return None

class Grid:
    def __init__(self, lines):
        self.octopi = []
        for line in lines:
            line = line.strip()
            row = []
            for char in line:
                row.append(Octopus(int(char)))
            self.octopi.append(row)

    def __str__(self):
        retval = ''
        for row in self.octopi:            
            for octopus in row:
                retval += str(octopus)
            retval += '\n'
        return retval
        
    def resetFlasing(self):
        for row in self.octopi:
            for octopus in row:
                octopus.isFlashing = False

    def takeStepAndReturnFlashCount(self):
        self.resetFlasing()
        for rowIndex, row in enumerate(self.octopi):
            for colIndex, octopus in enumerate(row):
                if octopus.increaseOrNone() is not None:
                    self.increaseNeighbors(rowIndex, colIndex)
        return self.countFlashes()

    def countFlashes(self):
        flashes = 0
        for row in self.octopi:
            for octopus in row:
                if octopus.isFlashing: flashes += 1
        return flashes

    def inbounds(self, newRow, newCol):
        return newRow >= 0 and newRow <= 9 and newCol >= 0 and newCol <= 9

    def increaseNeighbors(self, row, col):
        # print('increaseNeighbors(' + str(row) + ', ' + str(col) + ')')
        for key in DIRECTIONS:
            newRow = row + DIRECTIONS[key][0]
            newCol = col + DIRECTIONS[key][1]
            if self.inbounds(newRow, newCol):
                if self.octopi[newRow][newCol].increaseOrNone() is not None:
                    self.increaseNeighbors(newRow, newCol)

def main(): 
    with open('input') as f:
        lines = f.readlines()    
    grid = Grid(lines)
    numSteps = 100
    flashes = 0
    for i in range(numSteps):
        flashes += grid.takeStepAndReturnFlashCount()
        # print(grid)
    print(flashes)

    

    
    
if __name__ == '__main__':
    sys.exit(main())

