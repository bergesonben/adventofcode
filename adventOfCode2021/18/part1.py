import sys
import pytest

DEBUG = True

class SnailfishNumber():
    def __init__(self, *args):
        if (len(args) == 2):
            self.initFromRaw(args[0], args[1])
        elif (len(args) == 3):
            self.initFromExisting(args[0], args[1], args[2])
        else:
            raise Exception("Invalid number of args provied to SnailfishNumber constructor")

    def initFromExisting(self, parent, left, right):
        self.parent = parent
        self.isPair = True
        self.leftNum = left
        self.rightNum = right

    def initFromRaw(self, raw, parent): #raw is the string containing both the opening and closing brackets        
        self.parent = parent
        if ',' in raw: # is a pair
            raw = raw[1:-1]        
            self.isPair = True
            x = 0
            soFar = ''
            openBrackets = 0
            while True:
                if x == len(raw):
                    self.rightNum = SnailfishNumber(soFar, self)
                    break
                if raw[x] == '[': 
                    openBrackets += 1
                elif raw[x] == ']': 
                    openBrackets -= 1
                if raw[x] == ',' and openBrackets == 0:
                    self.leftNum = SnailfishNumber(soFar, self)
                    soFar = ''
                else:
                    soFar += raw[x]
                x +=1
        else: # is not a pair
            self.isPair = False
            self.leftNum = int(raw)
    
    def isLeftChild(self):
        return self.parent.leftNum == self

    def findLeftRealNumber(self):
        stack = [[self.parent, False, True, False]]
        if self.isLeftChild(): stack[0][1] = True
        while True:    
            currNum = stack[-1][0]        
            checkedLeft = stack[-1][1]
            checkedRight = stack[-1][2]      
            checkedParent = stack[-1][3]      
            if currNum is None: return None  

            if not checkedRight:
                if not currNum.rightNum.isPair:
                    return currNum.rightNum
                elif not checkedRight and currNum.rightNum.isPair:                
                    stack[-1][2] = True 
                    stack.append([currNum.rightNum, False, False, False])                     
            elif not checkedLeft:                      
                if not currNum.leftNum.isPair:
                    return currNum.leftNum
                elif currNum.isPair:
                    stack[-1][1] = True            
                    stack.append([currNum.leftNum, False, False, False])                    
            elif currNum.parent is None:
                stack.pop()         
            elif not checkedParent:                
                stack[-1][3] = True
                if not currNum.isLeftChild():                     
                    stack.append([currNum.parent, False, True, False])            
                else:
                    stack.append([currNum.parent, True, True, False])    
            else:
                stack.pop()  

            if len(stack) == 0: return None

    
    def findRightRealNumber(self):
        stack = [[self.parent, True, False, False]]
        if not self.isLeftChild(): stack[0][2] = True
        while True:    
            currNum = stack[-1][0]        
            checkedLeft = stack[-1][1]
            checkedRight = stack[-1][2]      
            checkedParent = stack[-1][3]      
            if currNum is None: return None  

            if not checkedLeft:                      
                if not currNum.leftNum.isPair:
                    return currNum.leftNum
                elif currNum.isPair:
                    stack[-1][1] = True
                    stack.append([currNum.leftNum, False, False, False])                    
            elif not checkedRight:
                if not currNum.rightNum.isPair:
                    return currNum.rightNum
                elif not checkedRight and currNum.rightNum.isPair:                
                    stack[-1][2] = True  
                    stack.append([currNum.rightNum, False, False, False])
            elif currNum.parent is None:
                stack.pop()         
            elif not checkedParent:                
                stack[-1][3] = True
                if currNum.isLeftChild():                     
                    stack.append([currNum.parent, True, False, False])            
                elif not currNum.isLeftChild():
                    stack.append([currNum.parent, True, True, False])    
            else:
                stack.pop()  

            if len(stack) == 0: return None

    def explode(self):
        leftRealNumber = self.findLeftRealNumber()
        if leftRealNumber is not None: leftRealNumber.leftNum += self.leftNum.leftNum
        rightRealNumber = self.findRightRealNumber()
        if rightRealNumber is not None: rightRealNumber.leftNum += self.rightNum.leftNum
        self.isPair = False
        self.rightNum = None
        self.leftNum = 0
        return bool(leftRealNumber or rightRealNumber)

    def explodeOrNone(self):
        stack = [[self, False, False]]
        currDepth = 0
        while True:            
            current = stack[-1]
            if currDepth == 4 and current[0].isPair:
                return current[0].explode()
            if current[0].isPair and not current[1]:
                current[1] = True
                stack.append([current[0].leftNum, False, False])
                currDepth += 1
            elif current[0].isPair and not current[2]:
                current[2] = True
                stack.append([current[0].rightNum, False, False])
                currDepth += 1
            else:
                currDepth -= 1
                stack.pop()
            if len(stack) == 0: return

    def split(self):
        self.isPair = True
        isOdd = bool(self.leftNum % 2)
        leftNum = self.leftNum // 2
        rightNum = leftNum + 1 if isOdd else leftNum
        self.leftNum = SnailfishNumber(str(leftNum), self)
        self.rightNum = SnailfishNumber(str(rightNum), self)
        return True
    
    def splitOrNone(self):
        stack = [[self, False, False]]
        while True:            
            currNum = stack[-1][0]
            checkedLeft = stack[-1][1]
            checkedRight = stack[-1][2]      
            if currNum.isPair:
                if not checkedLeft:
                    stack[-1][1] = True
                    stack.append([currNum.leftNum, False, False])
                elif not checkedRight:
                    stack[-1][2] = True
                    stack.append([currNum.rightNum, False, False])
                else:
                    stack.pop()
            else:
                if currNum.leftNum >= 10:
                    return currNum.split()
                else:
                    stack.pop()
            if len(stack) == 0: return
    
    def reduce(self):
        if self.explodeOrNone(): 
            if DEBUG: print('after explode: ' + str(self))
            return self.reduce()
        if self.splitOrNone(): 
            if DEBUG: print('after split: ' + str(self))
            return self.reduce()
        return
            

    def __str__(self):
        if self.isPair: return '[' + str(self.leftNum) + ',' + str(self.rightNum) + ']'
        else: return str(self.leftNum)      

    def add(self, other):
        newRoot = SnailfishNumber(None, self, other)        
        self.parent = newRoot
        other.parent = newRoot
        newRoot.reduce()
        return newRoot

    def getMagnitude(self):
        if self.isPair:
            return self.leftNum.getMagnitude() * 3 + self.rightNum.getMagnitude() * 2
        else:
            return self.leftNum

def main(): 
    global DEBUG    
    DEBUG = True if '-d' in sys.argv else False
    
    if 'test' in sys.argv:
        runTests()
    else:
        actualInput = []
        with open('/home/benjamin/Documents/adventOfCode2021/18/input') as f:
            lines = f.readlines()  
        for line in lines:
            if not line.isspace() and line[0] != '#': actualInput.append(line.strip()) 
        
        root = SnailfishNumber(actualInput[0], None) 
        actualInput.pop(0)
        for line in actualInput:
            root = root.add(SnailfishNumber(line, None))
        
        print(root.getMagnitude())
    

def testExplode():
    print('======Testing Explode======')
    testCases = [
        ('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
        ('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'), 
        ('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
        ('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'),
        ('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
        ('[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[0,[11,3]],[[6,3],[8,8]]]]]', '[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[11,0],[[9,3],[8,8]]]]]')
    ]
    try:
        for testCase in testCases:
            print('testing: ' + str(testCase))            
            root = SnailfishNumber(testCase[0], None)
            root.explodeOrNone()
            output = str(root)
            assert output == testCase[1], 'Expected ' + testCase[1] + ' got ' + output
            print('passed')

    except Exception as e:
        print("failed on testcase: " + str(testCase))
        print(e)



def testSplit():
    print('======Testing Split======')
    testCases = [
        ('[[[[0,7],4],[15,[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'),
        ('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]', '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]')
    ]
    try:
        for testCase in testCases:
            print('testing: ' + str(testCase))            
            root = SnailfishNumber(testCase[0], None)
            root.splitOrNone()
            output = str(root)
            assert output == testCase[1], 'Expected ' + testCase[1] + ' got ' + output
            print('passed')
    except Exception as e:
        print("failed on testcase: " + str(testCase))
        print(e)

def testReduce():
    print('======Testing Reduce======')
    testCases = [
        ('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'),
        ('[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]', '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]')
    ]
    try:
        for testCase in testCases:
            print('testing: ' + str(testCase))            
            root = SnailfishNumber(testCase[0], None)
            root.reduce()
            output = str(root)
            assert output == testCase[1], 'Expected ' + testCase[1] + ' got ' + output
            print('passed')
    except Exception as e:
        print("failed on testcase: " + str(testCase))
        print(e)

def testAdd():
    print('======Testing Add======')
    testCases = [
        ('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'),
    ]
    try:
        for testCase in testCases:
            print('testing: ' + str(testCase))            
            root = SnailfishNumber(testCase[0], None)
            root = root.add(testCase[1])
            output = str(root)
            assert output == testCase[1], 'Expected ' + testCase[1] + ' got ' + output
            print('passed')
    except Exception as e:
        print("failed on testcase: " + str(testCase))
        print(e)

def runTests():
        testExplode()
        testSplit()
        testReduce()
    
if __name__ == '__main__':
    sys.exit(main())