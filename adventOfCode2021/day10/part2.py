import sys
POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}
# PAREN_POINTS = 1
# BRACKET_POINTS = 2
# CURLY_BRACE_POINTS = 3
# ANGLE_BRACKET_POINTS = 4

def isOpening(char):
    return char == '(' or char == '[' or char == '{' or char == '<'

def getOpening(char):
    if char == ')':
        return '('
    elif char == '}':
        return '{'
    elif char == ']':
        return '['
    elif char == '>':
        return '<'

def getIllegalCharacterOrNone(line):
    line = line.strip()
    openings = []
    for char in line:
        if isOpening(char):
            openings.append(char)
        else:
            if openings[-1] == getOpening(char):
                openings.pop()
            else:
                return char
    return None

def getCompletingSequence(line):
    openings = []
    for char in line:
        if isOpening(char):
            openings.append(char)
        elif openings[-1] == getOpening(char):
            openings.pop()
    return list(reversed(openings))

def getScore(closings):
    score = 0
    for closing in closings:
        score = score * 5 + POINTS[closing]
    return score


def main(): 
    with open('test') as f:
        lines = f.readlines()
    
    incomplete = []
    for line in lines:
        if getIllegalCharacterOrNone(line) is None:
            incomplete.append(line)
    
    scores = []
    for line in incomplete:
        scores.append(getScore(getCompletingSequence(line)))
    
    length = len(scores)
    index = length // 2
    print(sorted(scores)[index])
    


    
    
if __name__ == '__main__':
    sys.exit(main())

