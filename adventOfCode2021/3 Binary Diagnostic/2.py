import sys
    
def getMostCommonBit(i, arr):        
    zeroes = 0
    ones = 0
    for bits in arr:
        if bits[i] == 0:
            zeroes += 1
        if bits[i] == 1:
            ones += 1        
    
    if zeroes > ones:
        return 0
    else:
        return 1

def getRating(isOxygen, binaries):
    oldList = binaries
    newList = []
    numDigits = len(binaries[0])
    for i in range(numDigits):
        if isOxygen:
            yeet = getMostCommonBit(i, oldList)
        else:
            yeet = int(not bool(getMostCommonBit(i, oldList)))
        for binary in oldList:
            if binary[i] == yeet:
                newList.append(binary)
        oldList = newList
        newList = []
        if len(oldList) == 1:
            return oldList[0]

def convertArrayOfBitsToInt(bits):
    foo = ""
    for bit in bits:
        foo += str(bit)
    return int(foo, 2)
    
def main(): 
    with open('input') as f:
        lines = f.readlines()
        binaries = []
        for line in lines:
            binaries.append([int(c) for c in line.strip()])
        oxygen = convertArrayOfBitsToInt(getRating(True, binaries))
        co = convertArrayOfBitsToInt(getRating(False, binaries))
        print("oxygen: " + str(oxygen) + "; co2: " + str(co) + "; result: " + str(oxygen * co))

if __name__ == '__main__':
    sys.exit(main())