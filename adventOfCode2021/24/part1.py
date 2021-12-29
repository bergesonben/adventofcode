import sys
import copy

INPUT = '/home/benjamin/Documents/adventOfCode2021/24/input'

def ALU(instructions, z, w):
    VARIABLES = {
        'x': 0,
        'y': 0, 
        'z': z,
        'w': w
    }
    for line in instructions:
        line = line.strip().split()
        if line[0] == 'inp':
            continue
        elif line[0] == 'add':   
            if line[2] in VARIABLES:
                if VARIABLES[line[1]] == 0 and VARIABLES[line[2]] == 0:
                    continue
                elif VARIABLES[line[1]] != 0 and VARIABLES[line[2]] == 0:
                    continue
                elif VARIABLES[line[1]] == 0 and VARIABLES[line[2]] != 0:
                    VARIABLES[line[1]] =  VARIABLES[line[2]]
                else:
                    VARIABLES[line[1]] = VARIABLES[line[1]] + VARIABLES[line[2]]
            elif line[2] != '0':                
                VARIABLES[line[1]] = VARIABLES[line[1]] + int(line[2])
        elif line[0] == 'mul':
            if line[2] in VARIABLES:
                if VARIABLES[line[1]] == 0 or VARIABLES[line[2]] == 0:
                    VARIABLES[line[1]] = 0
                else:
                    VARIABLES[line[1]] = VARIABLES[line[1]] * VARIABLES[line[2]]
            elif line[2] == '0':
                VARIABLES[line[1]] = 0
            else:
                VARIABLES[line[1]] = VARIABLES[line[1]] * int(line[2])
        elif line[0] == 'div':
            if line[2] in VARIABLES:
                VARIABLES[line[1]] = VARIABLES[line[1]] // VARIABLES[line[2]]
            elif line[2] != '1':
                VARIABLES[line[1]] = VARIABLES[line[1]] // int(line[2])
        elif line[0] == 'mod':
            if line[2] in VARIABLES:
                if VARIABLES[line[1]] == 0 and VARIABLES[line[2]] == 0:
                    continue
                elif VARIABLES[line[1]] != 0 and VARIABLES[line[2]] == 0:
                    VARIABLES[line[1]] = 0
                elif VARIABLES[line[1]] == 0 and VARIABLES[line[2]] != 0:
                    VARIABLES[line[1]] =  VARIABLES[line[2]]
                else:
                    VARIABLES[line[1]] = VARIABLES[line[1]] % VARIABLES[line[2]]
            else:
                VARIABLES[line[1]] = VARIABLES[line[1]] % int(line[2])
        elif line[0] == 'eql':
            if line[2] in VARIABLES:
                VARIABLES[line[1]] = int(VARIABLES[line[1]] == VARIABLES[line[2]])
            else:
                VARIABLES[line[1]] = int(VARIABLES[line[1]] == int(line[2]))
        else:
            raise Exception("unexpected item in bagging area")
    return VARIABLES['z']

def bullshit(lines, outputs):
    meh = set()
    for output in outputs.values():
        meh = meh.union(output)
    outputs = meh
    a = int(lines[-3].strip().split()[2])
    b = int(lines[3].strip().split()[2])
    c = int(lines[4].strip().split()[2])
    inputs = {}    
    for w in range(1,10):        
        x1s = set()
        x0s = set()
        for i in range(0,26):
            if (i + c) != w:
                x1s.add(i)
            else:
                x0s.add(i)
        for output in outputs:
            for x0 in x0s:
                meh = output * b
                if w in inputs:
                    inputs[w].add(meh+x0)
                else:
                    inputs[w] = {meh+x0}
            for x1 in x1s:
                meh = (output - w - a) / b
                if isinstance(meh, float):
                    continue
                    # raise Exception("false assumption")
                if w in inputs:
                    inputs[w].add(meh+x1)
                else:
                    inputs[w] = {meh+x1}
                input.add(meh+x1)
    return inputs

def main(): 
    with open(INPUT) as f:
        lines = f.readlines()

    digits = []
    linesSoFar = []
    for line in lines[1:]:
        if line.split()[0] == 'inp':
            digits.append(linesSoFar)
            linesSoFar = []
        else:
            linesSoFar.append(line)
    digits.append(linesSoFar)
    digitsReversed = reversed(digits)
        
    
    
    # for digit in digits:
    #     inputs = bullshit(digit, possibleOutputValues[-1])
    #     for key, values in inputs.items():
    #         for value in values:
    #             meh = set()
    #             for yeet in possibleOutputValues[-1].values():
    #                 meh = meh.union(yeet)
                
    #             if not ALU(digit, value, key) in meh:
    #                 print('ERROR')        
    #     possibleOutputValues.append(inputs)
    # print('success')
    # print(possibleOutputValues)

    possibleOutputValues = [{0:{0}}]
    for i, digit in enumerate(digitsReversed):               
        rangeMin = rangeMax = 0        
        a = int(digit[-3].strip().split()[2])
        b = int(digit[3].strip().split()[2])
        rangeMin = min(possibleOutputValues[-1].keys()) - a - 10
        rangeMax = (max(possibleOutputValues[-1].keys())+1) * b + 26
        print('checking ' + str(i) + ' min: ' + str(rangeMin) + ' max: ' + str(rangeMax)) 
        foo = {}
        minDigit = 10
        for w in range(9,0,-1):      
            if i == 13:
                p = ALU(digit, 0, w)
                if p in possibleOutputValues[-1]:
                    minDigit = min(minDigit, w)
                continue
            for z in range(rangeMin, rangeMax+1):
                if ALU(digit, z, w) in possibleOutputValues[-1]:
                    if z in foo: 
                        foo[z].add(w)
                    else:
                        foo[z] = {w}
        possibleOutputValues.append(foo) 

    possibleOutputValues.pop()
    answer = str(minDigit)
    z = 0
    for i, digitAnswer in enumerate(reversed(possibleOutputValues)):
        print(answer)
        z = ALU(digits[i], z, minDigit)        
        minDigit = min(digitAnswer[z])
        answer += str(minDigit)
    print(answer)



    


if __name__ == '__main__':
    sys.exit(main())

