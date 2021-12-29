import sys

class Board:
    def __init__(self, raw):
        self.boardSpots = []
        self.dict = {}
        self.isWon = False
        for i, row in enumerate(raw):
            rowNums = row.split()
            foo = []
            for j, num in enumerate(rowNums):
                foo.append(BoardSpot(num))
                self.dict[num] = (i,j)
            self.boardSpots.append(foo)                    

    def __str__(self):
        retVal = ""
        for row in self.boardSpots:
            retVal += (str(row[0]) + "\t" + str(row[1]) + "\t" + str(row[2]) + "\t" + str(row[3]) + "\t" + str(row[4]) + "\t\n")
            
        return retVal

    def markSpot(self, val):
        if str(val) in self.dict:
            coor = self.dict[str(val)]
            self.boardSpots[coor[0]][coor[1]].marked = True

    def getIsWon(self):
        for row in self.boardSpots:
            contiugousRow = True
            for val in row:
                if not val.marked:
                    contiugousRow = False
            if contiugousRow: 
                self.isWon = True

        for i in range(5):
            contiugousCol = True
            for row in self.boardSpots:
                if not row[i].marked:
                    contiugousCol = False
            if contiugousCol:
                self.isWon = True
        
        return self.isWon

    def getUnmarkedSum(self):
        unmarkedSum = 0
        for row in self.boardSpots:
            for col in row:
                if not col.marked:
                    unmarkedSum += int(col.val)
        return unmarkedSum

    def calculateScore(self, val):
        unmarkedSum = self.getUnmarkedSum()
        print("unmarkedSum: " + str(unmarkedSum) + "; move value: " + str(val) + "; result: " + str(unmarkedSum*val))

class BoardSpot:
    def __init__(self, val):
        self.val = val
        self.marked = False

    def __str__(self):        
        if self.marked:
            return '\033[92m' + str(self.val) + '\033[0m'
        else:
            return str(self.val)

def getInputsAndBoards():
    inputs = []
    boards = []

    with open('input') as f:
        lines = f.readlines()
        inputs = [int(i) for i in lines[0].split(",")]
        lines.pop(0) # removes inputs line
        lines.pop(0) # removes blank line
        
        for i in range(0, len(lines), 6):
            boards.append(Board([lines[i], lines[i+1], lines[i+2], lines[i+3], lines[i+4]]))

    return inputs, boards

def main(): 
    inputs, boards = getInputsAndBoards()
    
    for move in inputs:
        print("move: " + str(move))
        for board in boards:
            print(board)
        markedForPopping = []
        for i, board in enumerate(boards):
            board.markSpot(move)
            if board.getIsWon():   
                if len(boards) == 1:
                    board.calculateScore(move)
                    return
                markedForPopping.append(i)
                print("board #" + str(i+1) + " is eliminated")                                
        for i in reversed(markedForPopping):
            boards.pop(i)
if __name__ == '__main__':
    sys.exit(main())

