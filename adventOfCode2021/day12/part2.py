import sys
doubleVisited = False

class Cave():
    def __init__(self, raw):
        self.raw = raw
        self.isUpper = raw.isupper()
        self.visitedCount = 0
        self.connections = []
        self.isSpecial = False

    def addConnection(self, cave):
        self.connections.append(cave)

    def __eq__(self, other):
        if isInstance(other, Cave):
            return self.raw == other.raw
        return False
    
    def visit(self):
        if self.isUpper: return
        else: 
            self.visitedCount += 1

    def canVisitAgain(self):
        if self.isUpper: return True
        elif self.isSpecial and self.visitedCount < 2: return True
        else: return self.visitedCount < 1

    def unVisit(self):
        if self.isUpper: return
        else: self.visitedCount -= 1

def returnPaths(caves, startPoint):    
    global doubleVisited

    if not startPoint.canVisitAgain(): 
        if startPoint.raw != 'end' and startPoint.raw != 'start' and not doubleVisited:
            doubleVisited = True
            startPoint.isSpecial = True
            caves[startPoint.raw].visit()
            paths = []
            for connection in caves[startPoint.raw].connections:                        
                # print('coming from ' + startPoint.raw +'. going to ' + connection.raw)
                newPaths = returnPaths(caves, connection)
                if newPaths: 
                    for newPath in newPaths:
                        paths.append(startPoint.raw + ',' + newPath)
            # print('returnNumPaths(' + startPoint.raw + '): ' + str(numPaths))
            caves[startPoint.raw].unVisit()
            startPoint.isSpecial = False
            doubleVisited = False
            return paths
        return False
    if startPoint.raw == 'end': return ['end']    
    caves[startPoint.raw].visit()
    paths = []
    for connection in caves[startPoint.raw].connections:                        
        # print('coming from ' + startPoint.raw +'. going to ' + connection.raw)
        newPaths = returnPaths(caves, connection)
        if newPaths: 
            for newPath in newPaths:
                paths.append(startPoint.raw + ',' + newPath)
    # print('returnNumPaths(' + startPoint.raw + '): ' + str(numPaths))
    caves[startPoint.raw].unVisit()
    return paths

def returnNumPaths(caves, startPoint):    
    if startPoint.raw == 'end': return 1
    if not startPoint.canVisitAgain(): return 0
    caves[startPoint.raw].visit()
    numPaths = 0
    for connection in caves[startPoint.raw].connections:                        
        # print('coming from ' + startPoint.raw +'. going to ' + connection.raw)
        numPaths += returnNumPaths(caves, connection)
    print('returnNumPaths(' + startPoint.raw + '): ' + str(numPaths))
    caves[startPoint.raw].unVisit()
    return numPaths

def clearVisited(caves):
    for key in caves:
        caves[key].visitedCount = 0

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

    answer = returnPaths(caves, caves['start'])
    # print('----------------------------')
    # for key in caves:
    #     clearVisited(caves)
    #     if key != 'start' and key != 'end' and not caves[key].isUpper:
    #         caves[key].isSpecial = True
    #         answer += returnNumPaths(caves, caves['start'])
    #         break

    
    print(len(answer))


    
if __name__ == '__main__':
    sys.exit(main())

