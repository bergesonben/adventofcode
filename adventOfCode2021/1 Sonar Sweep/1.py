with open('input') as f:
    lines = f.readlines()
    prevDepth = 0
    numIncrease = -1
    for depth in lines:
        if prevDepth < int(depth):
            numIncrease += 1
        prevDepth = int(depth)
    print(numIncrease)
    