import sys
from math import ceil

def main(): 
    with open('input') as f:
        lines = f.readlines()  
    sequenceRaw = lines[0].strip()
    sequence = {}
    for i, char in enumerate(sequenceRaw):
        if i < len(sequenceRaw)-1:
            key = char + sequenceRaw[i+1]
            if key in sequence:
                sequence[key] += 1
            else:
                sequence[key] = 1
    mappings = {}
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        parsed = line.split('->')
        mappings[parsed[0].strip()] = parsed[1].strip()

    numSteps = 40

    for i in range(numSteps):
        newSequence = {}
        for key, value in sequence.items():
            newChar = mappings[key]
            newPair1 = key[0] + newChar
            newPair2 = newChar + key[1]
            if newPair1 in newSequence:
                newSequence[newPair1] += value
            else:
                newSequence[newPair1] = value
            if newPair2 in newSequence:
                newSequence[newPair2] += value
            else:
                newSequence[newPair2] = value
        sequence = newSequence

    charCounts = {}
    for key, value in sequence.items():
        if key[0] in charCounts:
            charCounts[key[0]] += value
        else:
            charCounts[key[0]] = value
        if key[1] in charCounts:
            charCounts[key[1]] += value
        else:
            charCounts[key[1]] = value
    for key, value in charCounts.items():
        charCounts[key] = ceil(value / 2)


    maxCount = max(charCounts.values())
    minCount = min(charCounts.values())
    print(maxCount-minCount)
    
if __name__ == '__main__':
    sys.exit(main())

