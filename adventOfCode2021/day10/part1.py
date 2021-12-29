import sys
PAREN_POINTS = 3
BRACKET_POINTS = 57
CURLY_BRACE_POINTS = 1197
ANGLE_BRACKET_POINTS = 25137

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

def main(): 
    with open('input') as f:
        lines = f.readlines()
    
    points = 0
    for line in lines:
        illegalChar = getIllegalCharacterOrNone(line)
        if illegalChar is None:
            continue
        elif illegalChar == ')':
            points += PAREN_POINTS
        elif illegalChar == ']':
            points += BRACKET_POINTS
        elif illegalChar == '}':
            points += CURLY_BRACE_POINTS
        elif illegalChar == '>':
            points += ANGLE_BRACKET_POINTS
    
    print(points)


    
    
if __name__ == '__main__':
    sys.exit(main())

