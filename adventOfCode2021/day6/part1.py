import sys

def main(): 
    with open('test') as f:
        lines = f.readlines()
        myList = [int(i) for i in lines[0].split(',')]
    
    numDays = 256
    for i in range(numDays):
        toBeAdded = 0
        for index, val in enumerate(myList):
            if val > 0:
                myList[index] -= 1
            if val == 0:
                myList[index] = 6
                toBeAdded += 1
        for j in range(toBeAdded):
            myList.append(8)
        print('after ' + str(i+1) + ' days: ')# + str(myList))
    print(len(myList))
    
    
if __name__ == '__main__':
    sys.exit(main())

