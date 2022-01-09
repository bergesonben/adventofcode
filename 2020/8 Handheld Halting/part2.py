from copy import deepcopy

def getInstructionValue(line):
    return int(line[3:])

def getAllVariations(lines):
    variations = []
    for i, line in enumerate(lines):
        if line[:3] == 'nop':
            variation = deepcopy(lines)
            variation[i] = line.replace('nop', 'jmp')
            variations.append(variation)
        elif line[:3] == 'jmp':
            variation = deepcopy(lines)
            variation[i] = line.replace('jmp', 'nop')
            variations.append(variation)
    return variations

def main(input):
    with open(input) as f:
        lines = f.readlines()

    variations = getAllVariations(lines)
    for variation in variations:
        visited = set()
        currLine = 0
        accumulator = 0
        foundError = False
        while not currLine in visited:
            if currLine == len(variation):
                foundError = True
                break
            visited.add(currLine)
            if variation[currLine][:3] == 'nop':
                currLine += 1
            elif variation[currLine][:3] == 'acc':
                accumulator += getInstructionValue(variation[currLine])
                currLine += 1
            elif variation[currLine][:3] == 'jmp':
                currLine += getInstructionValue(variation[currLine])
            else:
                raise Exception('Unexpected item in bagging area')
        if foundError:
            print(accumulator)
            break
    