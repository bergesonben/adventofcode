with open('day 1 input') as f:
    lines = f.readlines()
    depths = [int(line.strip()) for line in lines]    
    prevSum = 0
    numIncrease = -1
    counter = 0
    for i, depth in enumerate(depths, start=0):        
        if i >= len(depths)-2:
            break
        counter += 1
        sum = depth + depths[i+1] + depths[i+2]            
        # print("prevSum=" + str(prevSum) + ": " + str(depth) + "+" + str(depths[i+1]) + "+" + str(depths[i+2]) + "=" + str(sum))
        if sum > prevSum:
            numIncrease += 1
        prevSum = sum    
    print(numIncrease)