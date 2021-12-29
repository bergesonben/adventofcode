import sys

# targetXBegin = 20
# targetXEnd = 30
# targetYBegin = -5
# targetYEnd = -10

targetXBegin = 128
targetXEnd = 160
targetYBegin = -88 
targetYEnd = -142

def inRange(x, y):
    return x >= targetXBegin and x <= targetXEnd and y >= targetYEnd and y <= targetYBegin

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
    highestY = max(0, y)
    while keepGoing(position[0], position[1]):        
        (position, x, y) = step(x, y, position)
        highestY = max(position[1], highestY)
        if inRange(position[0], position[1]):
            return highestY
    return

def willGetInRange(x, y):
    position = (x, y)
    while keepGoing(position[0], position[1]):        
        if inRange(position[0], position[1]):
            return True
        (position, x, y) = step(x, y, position)
        
    return False

def main(): 
    answer = 0
    answers = []
    for x in range(1, targetXEnd+1):
        for y in range(targetYEnd, 1000):
            if willGetInRange(x, y): 
                answer += 1
                answers.append((x,y))
    
    print(answer)

    # correct = set()
    # with open('/home/benjamin/Documents/adventOfCode2021/17/test') as f:
    #     lines = f.readlines()  
    # for line in lines:
    #     pairs = line.split()
    #     for pair in pairs:
    #         clean = pair.strip().split(',')
    #         x = int(clean[0].strip())
    #         y = int(clean[1].strip())
    #         correct.add((x, y))
    # tempSet = set(answers)
    # print(correct - tempSet)

if __name__ == '__main__':
    sys.exit(main())


