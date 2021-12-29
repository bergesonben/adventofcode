import sys

def main(): 
    with open('input') as f:
        lines = f.readlines()
        myList = [int(i) for i in lines[0].split(',')]
    
    myDict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for val in myList:
        if val in myDict:
            myDict[val] += 1
        else:
            myDict[val] = 1
    # print(myDict)
    numDays = 256
    for i in range(numDays):
        newDict = myDict.copy()
        for j in range(8, -1, -1):                        
            if j in myDict:
                if j != 0:
                    myDict[j-1] = newDict[j]
                else:
                    myDict[8] = newDict[j]
                    myDict[6] += newDict[j]
        # print('after ' + str(i+1) + ' days: ' + str(myDict))
    
    count = 0
    for days in myDict:
        count += myDict[days]

    print(count)


    
    
    
if __name__ == '__main__':
    sys.exit(main())

