import sys

SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
GREATER_THAN = 5
LESS_THAN = 6
EQUAL_TO = 7

class OperatorPacket:
    def __init__(self, binary):        
        self.versionNumber = int(binary[0:3], 2)
        self.type = int(binary[3:6], 2)
        self.lenTypeId = binary[6]
        self.length = int(binary[7:22], 2) if self.lenTypeId == '0' else int(binary[7:18], 2)
        x = 22 if self.lenTypeId == '0' else 18
        self.children = []
        if self.lenTypeId == '0':               
            self.packetLen = x + self.length
            while x < self.packetLen:
                newChild  = LiteralPacket(binary[x:]) if int(binary[x+3:x+6], 2) == 4 else OperatorPacket(binary[x:])
                self.children.append(newChild)
                x += newChild.packetLen            
        else:            
            for i in range(self.length):
                newChild  = LiteralPacket(binary[x:]) if int(binary[x+3:x+6], 2) == 4 else OperatorPacket(binary[x:])
                self.children.append(newChild)
                x += newChild.packetLen
            self.packetLen = x

    def getVersionNumbers(self):
        answer = self.versionNumber
        for child in self.children:
            answer += child.getVersionNumbers()
        return answer
    
    def __str__(self):
        return 'OperatorPacket - versionNumber: ' + str(self.versionNumber) + ', type: ' + str(self.type) + ', lengthTypeId: ' + self.lenTypeId + ', length: ' + str(self.length) + ', numChildren: ' + str(len(self.children))

    def printEverything(self):
        print(self)
        for child in self.children:
            child.printEverything()

    def evaluate(self):
        answer = 0
        if self.type == SUM:
            for child in self.children:
                answer += child.evaluate()
        elif self.type == PRODUCT:
            if len(self.children) == 1: 
                answer = self.children[0].evaluate()
            else:
                answer = 1
                for child in self.children:
                    answer *= child.evaluate()
        elif self.type == MINIMUM:
            childVals = [child.evaluate() for child in self.children]
            answer = min(childVals)
        elif self.type == MAXIMUM:
            childVals = [child.evaluate() for child in self.children]
            answer = max(childVals)
        elif self.type == GREATER_THAN:
            answer = 1 if self.children[0].evaluate() > self.children[1].evaluate() else 0
        elif self.type == LESS_THAN:
            answer = 1 if self.children[0].evaluate() < self.children[1].evaluate() else 0
        elif self.type == EQUAL_TO:
            return int(self.children[0].evaluate() == self.children[1].evaluate())
        return answer
class LiteralPacket:
    def __init__(self, binary):        
        self.versionNumber = int(binary[0:3], 2)
        literalString = ''
        i = 6
        while True:
            literalString += binary[i+1:i+5]
            if binary[i] == '0': break            
            i += 5
        self.literal = int(literalString, 2)
        self.packetLen = i + 5

    def getVersionNumbers(self):
        return self.versionNumber  

    def __str__(self):
        return 'LiteralPacket - versionNumber: ' + str(self.versionNumber) + ', literal: ' + str(self.literal) + ', packetLen: ' + str(self.packetLen)

    def printEverything(self):
        print(self)

    def evaluate(self):
        return self.literal

def main(): 
    with open('/home/benjamin/Documents/adventOfCode2021/16/input') as f:
        lines = f.readlines()  
    for line in lines:
        if line[0] != '#': break   
    cleanLine = line.strip()
    raw = bin(int(cleanLine, 16))[2:]     
    while len(raw) != len(cleanLine) * 4:
        raw = '0' + raw
    headPacket = OperatorPacket(raw)    
    headPacket.printEverything()    
    print(headPacket.evaluate())    

if __name__ == '__main__':
    sys.exit(main())

