import sys
import itertools

IS_TEST = True
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/22/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/22/input'
ON = 'on'
OFF = 'off'
X = 0
Y = 1
Z = 2

def main(): 
    global IS_TEST
    IS_TEST =  True if '-t' in sys.argv else False
    input = TEST_INPUT if IS_TEST else ACTUAL_INPUT
    with open(input) as f:
        lines = f.readlines()
    cube = {}
    for line in lines:
        temp = line.strip().split()
        turnOn = temp[0] == ON
        temp = [i[2:] for i in temp[1].split(',')]
        xtemp = temp[X].split('..')
        xbegin = int(xtemp[0])
        xend = int(xtemp[1])
        ytemp = temp[Y].split('..')
        ybegin = int(ytemp[0])
        yend = int(ytemp[1])
        ztemp = temp[Z].split('..')
        zbegin = int(ztemp[0])
        zend = int(ztemp[1])
        if not (-50 <= xbegin <= 50 and -50 <= xend <= 50 and -50 <= ybegin <= 50 and -50 <= yend <= 50 and -50 <= zbegin <= 50 and -50 <= zend <= 50):
            continue
        for x in range(xbegin, xend+1):
            for y in range(ybegin, yend+1):
                for z in range(zbegin, zend+1):
                    if (x,y,z) in cube:
                        if turnOn:
                            cube[(x,y,z)] = True
                        else:
                            del cube[(x,y,z)]
                    else:
                        if turnOn:
                            cube[(x,y,z)] = True
    print(len(cube))

if __name__ == '__main__':
    sys.exit(main())

