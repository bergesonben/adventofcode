import sys

class Cave():
    def __init__(self, raw):
        self.raw = raw
        self.isUpper = raw.isupper()
        self.hasBeenVisited = False
        self.connections = []

    def addConnection(self, cave):
        self.connections.append(cave)

    def __eq__(self, other):
        if isInstance(other, Cave):
            return self.raw == other.raw
        return False
    
    def visit(self):
        if self.isUpper: return
        else: self.hasBeenVisited = True


def clearVisited(caves):
    for cave in caves:
        caves[cave].hasBeenVisited = False

def returnNumPaths(caves, startPoint):        
    if startPoint.raw == 'end': return 1
    if startPoint.hasBeenVisited: return 0
    caves[startPoint.raw].visit()
    numPaths = 0
    for connection in caves[startPoint.raw].connections:                        
        # print('coming from ' + startPoint.raw +'. going to ' + connection.raw)
        numPaths += returnNumPaths(caves, connection)
    # print('returnNumPaths(' + startPoint.raw + '): ' + str(numPaths))
    caves[startPoint.raw].hasBeenVisited = False
    return numPaths

def main(): 
    with open('input') as f:
        lines = f.readlines()   
    caves = {}
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


    
if __name__ == '__main__':
    sys.exit(main())

