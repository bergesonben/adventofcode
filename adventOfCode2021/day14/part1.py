import sys

def main(): 
    with open('input') as f:
        lines = f.readlines()  
    charCounts = {}
    sequence = lines[0].strip()
    for char in sequence:
        if char in charCounts:
            charCounts[char] += 1            
        else:
            charCounts[char] = 1
    mappings = {}
    lines.pop(0)
    lines.pop(0)
    for line in lines:
        parsed = line.split('->')
        mappings[parsed[0].strip()] = parsed[1].strip()

    numSteps = 10
    for i in range(numSteps):
        insertions = []    
        for i, char in enumerate(sequence):
            if i >= len(sequence)-1:
                break
            twoChar = char + sequence[i+1]
            if twoChar in mappings:
                insertions.append((mappings[twoChar], i+1))
        for i, insert in enumerate(insertions):
            if insert[0] in charCounts:
                charCounts[insert[0]] += 1
            else:
                charCounts[insert[0]] = 1
            sequence = sequence[:(insert[1]+i)] + insert[0] + sequence[(insert[1]+i):]

    maxCount = max(charCounts.values())
    minCount = min(charCounts.values())
    print(maxCount-minCount)
    
if __name__ == '__main__':
    sys.exit(main())

