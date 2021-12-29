import sys

class OperatorPacket:
    def __init__(self, binary):        
        self.versionNumber = int(binary[0:3], 2)
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
        return 'OperatorPacket - versionNumber: ' + str(self.versionNumber) + ', lengthTypeId: ' + self.lenTypeId + ', length: ' + str(self.length) + ', numChildren: ' + str(len(self.children))

    def printEverything(self):
        print(self)
        for child in self.children:
            child.printEverything()

class LiteralPacket:
    def __init__(self, binary):        
        self.versionNumber = int(binary[0:3], 2)
        literalString = ''
        i = 6
        while True:
            literalString += str(int(binary[i:i+5], 2))
            if binary[i] == '0': break            
            i += 5
        self.literal = int(literalString)
        self.packetLen = i + 5

    def getVersionNumbers(self):
        return self.versionNumber  

    def __str__(self):
        return 'LiteralPacket - versionNumber: ' + str(self.versionNumber) + ', literal: ' + str(self.literal) + ', packetLen: ' + str(self.packetLen)

    def printEverything(self):
        print(self)

def main(): 
    with open('/home/benjamin/Documents/adventOfCode2021/16/input') as f:
        lines = f.readlines()  
    for line in lines:
        if line[0] != '#': break   
    raw = bin(int(line.strip(), 16))[2:]     
    while len(raw) % 4 != 0:
        raw = '0' + raw
    headPacket = OperatorPacket(raw)
    answer = headPacket.getVersionNumbers()
    # headPacket.printEverything()
    print(answer)    

if __name__ == '__main__':
    sys.exit(main())

