import sys
import itertools

IS_TEST = True
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/22/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/22/input'
ON = 'on'
OFF = 'off'
X = 0
Y = 1
Z = 2

class AxisRange:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def getOverlapOrNone(self, other):
        begin = max(self.begin, other.begin)
        end = min(self.end, other.end)
        if begin > end: return
        return AxisRange(begin, end)
    
    def getLength(self):
        return len(range(self.begin, self.end))+1

class Cube:
    def __init__(self, *args):
        if len(args) == 7:
            self.initWithBeginAndEnd(*args)
        elif len(args) == 4:
            self.initWithRange(*args)
        self.overlaps = set()
    
    def initWithBeginAndEnd(self, on, xbegin, xend, ybegin, yend, zbegin, zend):
        self.on = on
        self.x = AxisRange(xbegin, xend)
        self.y = AxisRange(ybegin, yend)
        self.z = AxisRange(zbegin, zend)
    
    def initWithRange(self, on, xRange, yRange, zRange):
        self.on = on
        self.x = xRange
        self.y = yRange
        self.z = zRange
    
    def getOverlapOrNone(self, other):
        xOverlap = self.x.getOverlapOrNone(other.x)
        yOverlap = self.y.getOverlapOrNone(other.y)
        zOverlap = self.z.getOverlapOrNone(other.z)
        if xOverlap is None or yOverlap is None or zOverlap is None:            
            return
        if self.on:
            if other.on:
                return Cube(False, xOverlap, yOverlap, zOverlap)
            else:
                return Cube(True, xOverlap, yOverlap, zOverlap)
        else:
            if other.on: 
                return Cube(False, xOverlap, yOverlap, zOverlap)
            else:
                return Cube(True, xOverlap, yOverlap, zOverlap)
    
    def getVolume(self):
        xLen = self.x.getLength()
        yLen = self.y.getLength()
        zLen = self.z.getLength()
        absVolume = xLen * yLen * zLen 
        return absVolume if self.on else -absVolume

def numLightsTurnedOn(prevCubes, cube):
    numLights = cube.getVolume() if cube.on else 0
    for prevCube in prevCubes:    
        if prevCube.on:
            # print('checking for overlaps between cube ' + cube.id + ' and cube ' + prevCube.id)        
            overlap = cube.getOverlapOrNone(prevCube)
            if overlap is None:
                continue        
            overlap.id = cube.id + '-' + prevCube.id
            cube.overlaps.add(overlap)
            # print('changed: ' + str(overlap.getVolume()))
            numLights += overlap.getVolume()
        for overlap in prevCube.overlaps:
            # print('checking for overlaps between cube ' + cube.id + ' and cube ' + overlap.id)
            newOverlap = cube.getOverlapOrNone(overlap)            
            if newOverlap is None:
                continue
            newOverlap.id = cube.id + '-' + overlap.id
            cube.overlaps.add(newOverlap)
            # print('changed: ' + str(newOverlap.getVolume()))
            numLights += newOverlap.getVolume()
        

    return numLights

def main(): 
    global IS_TEST
    IS_TEST =  True if '-t' in sys.argv else False
    input = TEST_INPUT if IS_TEST else ACTUAL_INPUT
    with open(input) as f:
        lines = f.readlines()
    cubes = []
    totalOn = 0
    for stepNum, line in enumerate(lines):
        temp = line.strip().split()
        turnOn = temp[0] == ON
        temp = [i[2:] for i in temp[1].split(',')]
        xtemp = temp[X].split('..')
        xbegin = int(xtemp[0])
        xend = int(xtemp[1])
        ytemp = temp[Y].split('..')
        ybegin = int(ytemp[0])
        yend = int(ytemp[1])
        ztemp = temp[Z].split('..')
        zbegin = int(ztemp[0])
        zend = int(ztemp[1])

        newCube = Cube(turnOn, xbegin, xend, ybegin, yend, zbegin, zend)
        newCube.id = str(stepNum + 1)
        numLights = numLightsTurnedOn(cubes, newCube)
        totalOn += numLights
        
        cubes.append(newCube)
        # print('on step ' + str(stepNum+1) + ' ' + str(numLights) + ' lights were turned on')
    print(totalOn)
        

if __name__ == '__main__':
    sys.exit(main())

