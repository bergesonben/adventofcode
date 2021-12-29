import sys
import collections

DEBUG = True
USE_CACHE = False
IS_TEST = True
CACHE_FILE = None
CACHE_FILE_TEST = '/home/benjamin/Documents/adventOfCode2021/20/test_cache'
CACHE_FILE_INPUT = '/home/benjamin/Documents/adventOfCode2021/20/test_cache2'
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/20/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/20/input'
DARK = '.'
LIGHT = '#'
DIRECTIONS = [(-1, -1),(-1, 0), (-1, 1), (0, -1), (0,0),(0, 1), (1, -1),(1, 0), (1, 1)]
ROW = 0
COL = 1

def pixelToBinary(pixelStr):
    binStr = ''
    for c in pixelStr:
        binStr += '0' if c == DARK else '1'
    bin = int(binStr, 2)
    return bin

def replaceCharInString(string, index, replacement):
    if index >= len(string):
        raise Exception('invalid index: ' + str(index) + '(str: ' + string + ',replacement: ' + replacement + ')')
    if index == len(string) - 1:
        return string[:index] + replacement
    else:
        return string[:index] + replacement + string[index + 1:]

class Algorithm:
    def __init__(self, raw):
        self.value = raw

    def get(self, index):
        if index < 0 or index >= len(self.value):
            raise Exception("Invalid index passed into Algorithm.get")
        return self.value[index]

    def run(self, image):
        image.expand()
        newImageVal = image.value.copy()        
        for row, rowStr in enumerate(image.value):
            for col in range(len(rowStr)):
                pixelStr = image.getSurroundingPixelsAsString(row, col)
                algoIndex = pixelToBinary(pixelStr)
                newPixelVal = self.get(algoIndex)
                newImageVal[row] = replaceCharInString(newImageVal[row], col, newPixelVal)
        image.value = newImageVal
        algoIndex = 511 if image.default == LIGHT else 0
        image.default = self.get(algoIndex)
    
class Image:
    def __init__(self, lines):
        self.value = [line.strip() for line in lines]            
        self.default = DARK

    def expand(self):
        topAndBottom = self.default * len(self.value[0])
        self.value.insert(0, topAndBottom)
        self.value.append(topAndBottom)
        for i,row in enumerate(self.value):
            self.value[i] = self.default + row + self.default
    
    def getSurroundingPixelsAsString(self, row, col):
        retval = ''
        for dir in DIRECTIONS:
            newRow = row + dir[ROW]
            newCol = col + dir[COL]
            if newRow < 0 or newRow >= len(self.value[0]) or newCol < 0 or newCol >= len(self.value):
                retval += self.default
            else:
                retval += self.value[newRow][newCol]
        return retval

    def numLitPixels(self):
        count = 0
        for row in self.value:
            count += row.count(LIGHT)
        return count 

    def print(self):
        for row in self.value:
            print(row)

def isDark(char):
    return char == DARK


def main(): 
    global DEBUG, USE_CACHE, IS_TEST, CACHE_FILE
    DEBUG = True if '-d' in sys.argv else False
    USE_CACHE = True if '-c' in sys.argv else False
    IS_TEST =  True if '-t' in sys.argv else False
    CACHE_FILE = CACHE_FILE_TEST if IS_TEST else CACHE_FILE_INPUT
  
    with open(TEST_INPUT if IS_TEST else ACTUAL_INPUT) as f:
        lines = f.readlines()  
    
    algorithm = Algorithm(lines[0].strip())
    lines.pop(0) # remove algorithm line
    lines.pop(0) # remove blank space
    image = Image(lines)

    for i in range(50):
        print('running enhacement #' + str(i))
        algorithm.run(image)
        print('num lit pixels: ' + str(image.numLitPixels()))   

if __name__ == '__main__':
    sys.exit(main())

