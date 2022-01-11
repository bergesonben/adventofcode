from itertools import combinations

def findInvalidNum(nums, preambleLen):
    lastIndex = preambleLen    
    while True:
        a = combinations(nums[lastIndex-preambleLen:lastIndex], 2)        
        isValid = False
        for b in a:
            if b[0] + b[1] == nums[lastIndex]:
                lastIndex += 1
                isValid = True
                break
        if not isValid:
            break

    return nums[lastIndex]

def main(input, isTest):
    with open(input) as f:
        lines = f.readlines()

    lines = [int(i) for i in lines]
    preambleLen = 5 if isTest else 25
    invalidNum = findInvalidNum(lines, preambleLen)
    
    found = False
    for i, num in enumerate(lines):  
        numsSoFar = {num}
        sumSoFar = num 
        offset = 1
        while sumSoFar < invalidNum:
            numsSoFar.add(lines[i+offset])
            sumSoFar += lines[i+offset]
            offset += 1
            if sumSoFar == invalidNum:
                found = True
                break
        if found:
            break
    
    print(min(numsSoFar) + max(numsSoFar))
   
    