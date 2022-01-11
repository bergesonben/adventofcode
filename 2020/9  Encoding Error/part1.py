from itertools import combinations

def main(input, isTest):
    with open(input) as f:
        lines = f.readlines()

    lines = [int(i) for i in lines]
    preambleLen = 5 if isTest else 25

    lastIndex = preambleLen    
    while True:
        a = combinations(lines[lastIndex-preambleLen:lastIndex], 2)        
        isValid = False
        for b in a:
            if b[0] + b[1] == lines[lastIndex]:
                lastIndex += 1
                isValid = True
                break
        if not isValid:
            break

    print(lines[lastIndex])
    