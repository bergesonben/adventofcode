import sys
import itertools

DEBUG = True
USE_CACHE = False
IS_TEST = True
CACHE_FILE_TEST = '/home/benjamin/Documents/adventOfCode2021/19/test_cache'
CACHE_FILE_INPUT = '/home/benjamin/Documents/adventOfCode2021/19/test_cache2'
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/19/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/19/input'
INVERSE = {0: 0,1:1,2:2,3:3,4:8,5:10,6:11,7:9,8:4,9:9,10:5,11:6,12:13,13:12,14:14,15:15,16:16,17:18,18:17,19:19,20:22,21:21,22:20,23:23}

X = 0
Y = 1
Z = 2

class Point:
    def __init__(self, *args):        
        if len(args) == 1:
            raw = args[0].strip().split(',')
            self.x = int(raw[0])
            self.y = int(raw[1])
            self.z = int(raw[2])
        elif len(args) == 3:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            raise Exception("invalid number of args passed into Point constructor")
    
    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ')'

    def getPermutation(self, index):
        newPoint = getPermutation(self, index)
        return Point(newPoint[X], newPoint[Y], newPoint[Z])
    
    def asTuple(self):
        return (self.x, self.y, self.z)

class Line:
    def __init__(self, *args):
        if(len(args) == 2):
            self.point1 = args[0]
            self.point2 = args[1]
            self.diff = (self.point1.x - self.point2.x, self.point1.y - self.point2.y, self.point1.z - self.point2.z)
        elif len(args) == 3:
            self.point1 = args[0]
            self.point2 = args[1]
            self.diff = args[2]
        else:
            raise Exception("Invalid number of args provied to Line constructor")

    def getPermutations(self):
        if hasattr(self, 'permutations'):
            return self.permutations

        permutations = []
        for i in range(24):
            permutations.append(Line(self.point1, self.point2, getPermutation(self, i)))
        self.permutations = permutations
        return permutations

    def isEqualAndShouldBeInverted(self, otherLine):
        negativeDiff = (0-self.diff[X], 0-self.diff[Y], 0-self.diff[Z])
        if self.diff == otherLine.diff:
            return (True, False)
        elif negativeDiff == otherLine.diff:
            return (True, True)
        else: 
            return (False, None)  
        
    def __str__(self):
        return str(self.point1) + '->' + str(self.point2)

class Relationship:
    def __init__(self, permutation, shift, scanner1, scanner2):
        self.permutation = permutation
        self.shift = shift
        self.scanner1 = scanner1
        self.scanner2 = scanner2
    
    def __str__(self):
        return '(' + str(self.permutation) + ',' + str(self.shift) + ',' + str(self.scanner1.id) + ',' + str(self.scanner2.id) + ')'

    def applyToPoint(self, point, shouldInvert):        
        if shouldInvert:
            shifted = Point(point.x - self.shift[X], point.y - self.shift[Y], point.z - self.shift[Z])
            rotated = shifted.getPermutation(INVERSE[self.permutation])            
            return rotated
        else:
            rotated = point.getPermutation(self.permutation)
            shifted = Point(rotated.x + self.shift[X], rotated.y + self.shift[Y], rotated.z + self.shift[Z])
            return shifted
    
    def getSharedBeacons(self):
        beacons = set()       
        rawBeacons = self.scanner2.beacons
        for rawBeacon in rawBeacons:
            beacons.add(self.applyToPoint(rawBeacon, False))        
        allBeacons = beacons.union(set(self.scanner1.beacons))

        allBeaconsReduced = set([(i.x, i.y, i.z) for i in allBeacons])
        return allBeaconsReduced


class Scanner:
    def __init__(self, points, id):
        self.beacons = points
        self.lines = self.getLines()
        self.relationships = set()
        self.id = id

    def getLines(self):
        lines = []
        for i, point in enumerate(self.beacons[:-1]):
            for j, otherPoint in enumerate(self.beacons[i+1:]):  
                line = Line(point, otherPoint)          
                lines.append(line)                
        return lines  

    def createRelationship(self, otherScanner):
        scanner1Lines = self.lines
        scanner2Lines = otherScanner.lines
        scannerLinesPermutations = []
        for line in scanner2Lines:
            scannerLinesPermutations.append(line.getPermutations())
        counts = {}
        hasAtleast12Overlapping = False
        for line1 in scanner1Lines:
            for line2 in scannerLinesPermutations:
                for i, permutation in enumerate(line2): 
                    diffIsEqual, shouldInvert = line1.isEqualAndShouldBeInverted(permutation)
                    if diffIsEqual:   
                        if not i in counts: counts[i] = 1
                        else: counts[i] += 1
                        if counts[i] >= 12: 
                            hasAtleast12Overlapping = True  
                            point1 = line1.point1
                            point2 = permutation.point2 if shouldInvert else permutation.point1                                    
                            permIndex = i
                            break
                if hasAtleast12Overlapping: break
            if hasAtleast12Overlapping: break             
                  
        if not hasAtleast12Overlapping: return 
                
        point2rotated = point2.getPermutation(permIndex)
        shift = (point1.x - point2rotated.x, point1.y - point2rotated.y, point1.z - point2rotated.z)
        # print('point1:' + str(point1))
        # print('point2:' + str(point2[0]))
        # print('point2Rotated:' + str(point2rotated))
        # print('shift:' + str(shift))
        newRelationship = Relationship(permIndex, shift, self, otherScanner)        
        self.relationships.add(newRelationship)
        otherScanner.relationships.add(newRelationship)

    def getAllBeacons(self, visited):
        beacons = set()       
        for relationship in self.relationships:
            otherScanner = relationship.scanner2 if relationship.scanner1 == self else relationship.scanner1
            if not otherScanner.id in visited:    
                visited.add(otherScanner.id)
                rawBeacons = otherScanner.getAllBeacons(visited)                        
                shouldInvert = False if relationship.scanner1 == self else True
                for rawBeacon in rawBeacons:
                    beacons.add(relationship.applyToPoint(rawBeacon, shouldInvert))        
        allBeacons = beacons.union(set(self.beacons))

        return allBeacons

    def getAllScanners(self, visited):
        scanners = set()       
        for relationship in self.relationships:
            otherScanner = relationship.scanner2 if relationship.scanner1 == self else relationship.scanner1
            if not otherScanner.id in visited:    
                visited.add(otherScanner.id)
                rawScanners = otherScanner.getAllScanners(visited)
                shouldInvert = False if relationship.scanner1 == self else True
                for rawScanner in rawScanners:
                    scanners.add(relationship.applyToPoint(rawScanner, shouldInvert))        
        allScanners = scanners.union(set([Point(0,0,0)]))

        return allScanners

def getPermutation(pointOrLine, index):
    if isinstance(pointOrLine, Point):
        coor = (pointOrLine.x, pointOrLine.y, pointOrLine.z)
    elif isinstance(pointOrLine, Line):
        coor = pointOrLine.diff
    else:
        raise Exception("invalid type passed into getPermutation")
    if index > 23: 
        raise Exception("invalid index passed into getPermutation")
    #inverse just apply again
    if index == 0: return (coor[X], coor[Y], coor[Z])
    elif index == 1: return (coor[X], 0-coor[Y], 0-coor[Z])
    elif index == 2: return (0-coor[X], coor[Y], 0-coor[Z])
    elif index == 3: return (0-coor[X], 0-coor[Y], coor[Z])    
    elif index == 4: return (coor[Y], coor[Z], coor[X]) #8
    elif index == 5: return (coor[Y], 0-coor[Z], 0-coor[X]) #10
    elif index == 6: return (0-coor[Y], coor[Z], 0-coor[X]) #11
    elif index == 7: return (0-coor[Y], 0-coor[Z], coor[X]) # 9
    elif index == 8: return (coor[Z], coor[X], coor[Y]) # 4
    elif index == 9: return (coor[Z], 0-coor[X], 0-coor[Y]) # 9
    elif index == 10: return (0-coor[Z], coor[X], 0-coor[Y]) # 5
    elif index == 11: return (0-coor[Z], 0-coor[X], coor[Y]) # 6
    elif index == 12: return (coor[X], coor[Z], 0-coor[Y]) # 13
    elif index == 13: return (coor[X], 0-coor[Z], coor[Y]) # 12
    elif index == 14: return (0-coor[X], coor[Z], coor[Y]) # 14
    elif index == 15: return (0-coor[X], 0-coor[Z], 0-coor[Y]) # 15
    elif index == 16: return (coor[Y], coor[X], 0-coor[Z]) # 16
    elif index == 17: return (coor[Y], 0-coor[X], coor[Z]) # 18
    elif index == 18: return (0-coor[Y], coor[X], coor[Z]) # 17
    elif index == 19: return (0-coor[Y], 0-coor[X], 0-coor[Z])# 19
    elif index == 20: return (coor[Z], coor[Y], 0-coor[X]) #22
    elif index == 21: return (coor[Z], 0-coor[Y], coor[X]) #21
    elif index == 22: return (0-coor[Z], coor[Y], coor[X]) # 20
    elif index == 23: return (0-coor[Z], 0-coor[Y], 0-coor[X]) # 23        


def writeToCache(scanners):
    f = open(CACHE_FILE_TEST if IS_TEST else CACHE_FILE_INPUT, 'w')
    relationships = []
    for scanner in scanners:
        relationships += list(scanner.relationships)
    for relationship in relationships:
        write = \
            str(relationship.permutation) + \
            ',' + str(relationship.shift[X]) + \
            ',' + str(relationship.shift[Y]) + \
            ',' + str(relationship.shift[Z]) + \
            ',' + str(relationship.scanner1.id) + \
            ',' + str(relationship.scanner2.id) + '\n'
        f.write(write)
        
def getNumberOfBeacons(scanners):                
    visited = set()
    visited.add(scanners[0].id)
    beacons = scanners[0].getAllBeacons(visited)      
    beaconsReduced = set([(i.x, i.y, i.z) for i in beacons])      
    return len(beaconsReduced)    

def createRelationships(scanners):
    x = 1
    for i, scanner1 in enumerate(scanners[:-1]):
        for scanner2 in scanners[i+1:]:
            print('creating relationship between scanner' + str(scanner1.id) + ' and scanner' + str(scanner2.id) + ' (' + str(x) + '/406) ...')
            scanner1.createRelationship(scanner2)
            x += 1    

def readFromCache(scanners):
    with open(CACHE_FILE_TEST if IS_TEST else CACHE_FILE_INPUT) as f:
            lines = f.readlines() 
    for line in lines:
        rawRel = [int(i) for i in line.strip().split(',')]
        scanner1 =  scanners[rawRel[4]]
        scanner2 =  scanners[rawRel[5]]
        newRel = Relationship(rawRel[0], (rawRel[1], rawRel[2], rawRel[3]), scanner1, scanner2)
        scanner1.relationships.add(newRel)
        scanner2.relationships.add(newRel)

def getLongestDistance(scanners):
    visited = set()
    visited.add(scanners[0].id)
    allScanners = scanners[0].getAllScanners(visited)      
    scannersReduced = set([(i.x, i.y, i.z) for i in allScanners])      
    combinations = itertools.combinations(scannersReduced, 2)

    maxDistance = 0
    for combination in combinations:
        distance = abs(combination[0][X] - combination[1][X]) + abs(combination[0][Y] - combination[1][Y]) + abs(combination[0][Z] - combination[1][Z])
        maxDistance = max(maxDistance, distance)

    return maxDistance

def main(): 
    global DEBUG, USE_CACHE, IS_TEST
    DEBUG = True if '-d' in sys.argv else False
    USE_CACHE = True if '-c' in sys.argv else False
    IS_TEST =  True if '-t' in sys.argv else False
    
    # if 'test' in sys.argv:
    #     runTests()
    # else:    
    
    with open(TEST_INPUT if IS_TEST else ACTUAL_INPUT) as f:
        lines = f.readlines()  
    scanners = []
    points = []
    id = 0
    for line in lines:
        if line[0:3] == '---': 
            points = []
        elif line.isspace(): 
            scanners.append(Scanner(points, id))
            id += 1
        else:
            points.append(Point(line))
    scanners.append(Scanner(points, id))

    if USE_CACHE:
        readFromCache(scanners)
    else:
        createRelationships(scanners)
        writeToCache(scanners)   
    
    print('maxDistance: ' + str(getLongestDistance(scanners)))
   


if __name__ == '__main__':
    sys.exit(main())

