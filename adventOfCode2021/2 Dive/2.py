DOWN = 'down'
UP = 'up'
FORWARD = 'forward'

with open('input') as f:
    lines = f.readlines()
    splitLines = [line.strip().split() for line in lines]   
    aim = 0
    depth = 0
    horizontalPos = 0
    for line in splitLines:
        if line[0] == DOWN:
            aim += int(line[1])
        if line[0] == UP:
            aim -= int(line[1])
        if line[0] == FORWARD:
            horizontalPos += int(line[1])
            depth += aim*int(line[1])
            
    print("depth = " + str(depth) + "; horizontalPos = " + str(horizontalPos) + "; result = " + str(depth * horizontalPos))
    
