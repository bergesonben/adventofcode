def getInstructionValue(line):
    return int(line[3:])

def main(input):
    with open(input) as f:
        lines = f.readlines()

    visited = set()
    currLine = 0
    accumulator = 0
    while not currLine in visited:
        visited.add(currLine)
        if lines[currLine][:3] == 'nop':
            currLine += 1
        elif lines[currLine][:3] == 'acc':
            accumulator += getInstructionValue(lines[currLine])
            currLine += 1
        elif lines[currLine][:3] == 'jmp':
            currLine += getInstructionValue(lines[currLine])
        else:
            raise Exception('Unexpected item in bagging area')

    print(accumulator)