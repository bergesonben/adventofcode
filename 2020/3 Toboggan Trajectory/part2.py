TREE = '#'
EMPTY = '.'
SLOPES = [(1,1),(1,3),(1,5),(1,7),(2,1)]
ROW = 0
COL = 1

class TreeMap:
    def __init__(self, lines):
        self.board = []
        row = []
        for line in lines:
            for c in line.strip():
                row.append(c)
            self.board.append(row)
            row = []
        self.height = len(self.board)
        self.width = len(self.board[0])

    def pastBottom(self,pos):
        return pos[ROW] >= self.height
        
    def getSpaceValue(self, pos):        
        return self.board[pos[ROW]][pos[COL] % self.width]

    def isTree(self, pos):
        return self.getSpaceValue(pos) == TREE

    def getNumTreesHit(self, slope):
        pos = (0,0)
        count = 0
        while not self.pastBottom(pos):
            if self.isTree(pos):
                count += 1
            pos = (pos[ROW] + slope[ROW], pos[COL] + slope[COL])
        return count

def main(input):
    with open(input) as f:
        lines = f.readlines()

    treeMap = TreeMap(lines)
    answer = 1
    for slope in SLOPES:
        answer *= treeMap.getNumTreesHit(slope)
    print(answer)    

