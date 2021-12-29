import sys
import time

class Cave():
    def __init__(self, raw):
        self.raw = raw
        self.isUpper = raw.isupper()
        self.hasBeenVisited = False
        self.connections = []

    def addConnection(self, cave):
        self.connections.append(cave)

    def __eq__(self, other):
        if isinstance(other, Cave):
            return self.raw == other.raw
        return False
    
    def visit(self):
        if self.isUpper: return
        else: self.hasBeenVisited = True


def clearVisited(caves):
    for cave in caves:
        caves[cave].hasBeenVisited = False

# def returnNumPaths(caves, startPoint):    
#     if startPoint.raw == 'end': return 1
#     if startPoint.hasBeenVisited: return 0
#     caves[startPoint.raw].visit()
#     numPaths = 0
#     for connection in caves[startPoint.raw].connections:                        
#         # print('coming from ' + startPoint.raw +'. going to ' + connection.raw)
#         numPaths += returnNumPaths(caves, connection)
#     # print('returnNumPaths(' + startPoint.raw + '): ' + str(numPaths))
#     caves[startPoint.raw].hasBeenVisited = False
#     return numPaths

def returnNumPaths(caves, startPoint):    
    count = 0
    stack = []
    stack.append(startPoint)
    while stack:        
        currCave = stack[-1]
        print('currCave: ' + currCave.raw)
        currCave.visit()                
        added = 0
        for connection in currCave.connections:                        
            if connection.raw == 'end':
                count += 1
            elif not connection.hasBeenVisited:
                added += 1
                stack.append(connection)     
        
        if (currCave == stack[-1]):
            currCave.hasBeenVisited = False
            stack.pop()
        else:
            stack.pop(-1-added)
            
        
    return count

def main(): 
    with open('/home/benjamin/Documents/adventOfCode2021/day12/test') as f:
        lines = f.readlines()   
    caves = {}
    startTime = time.time()
    for line in lines:
        connection = line.split('-')
        caveA = connection[0].strip()
        caveB = connection[1].strip()
        if caveA not in caves:
            caves[caveA] = Cave(caveA)
        if caveB not in caves:
            caves[caveB] = Cave(caveB)
        caves[caveA].addConnection(caves[caveB])
        caves[caveB].addConnection(caves[caveA])
    
    answer = returnNumPaths(caves, caves['start'])
    print(answer)
    print(time.time() - startTime)

    
if __name__ == '__main__':
    sys.exit(main())

