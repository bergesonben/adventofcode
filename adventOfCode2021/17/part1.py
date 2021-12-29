import sys

targetXBegin = 128
targetXEnd = 160
targetYBegin = -142
targetYEnd = -88
#x=128..160, y=-142..-88

def inRange(x, y):
    return x >= targetXBegin and x <= targetXEnd and y >= targetYBegin and y <= targetYEnd

def keepGoing(x, y):
    return x <= targetXEnd and y >= targetYEnd

def step(x, y, pos):
    newX = 0
    if x > 0: newX = x - 1
    elif x < 0: newX = x + 1
    newY = y - 1
    return ((pos[0] + newX, pos[1] + newY), newX, newY)

def getHighestPointOrNone(x, y):    
    position = (x, y)
    numSteps = 0
    highestY = max(0, y)
    while keepGoing(position[0], position[1]):        
        numSteps += 1
        (position, x, y) = step(x, y, position)
        highestY = max(position[1], highestY)
        if inRange(position[0], position[1]):
            return highestY
    return

def main(): 
    maxHigh = 0
    maxVelocity = (0, 0)
    for x in range(1, targetXEnd):
        for y in range(0, 1000):
            highOpt = getHighestPointOrNone(x, y)
            if highOpt and highOpt > maxHigh:
                maxHigh = highOpt
                maxVelocity = (x, y)

    
    print(maxHigh)
    print(maxVelocity)

if __name__ == '__main__':
    sys.exit(main())

