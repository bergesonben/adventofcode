import sys

def get1478(arr):
    retval = {}
    remainder = []
    for i in arr:
            if len(i) == 2:
                retval[1] = i
            elif len(i) == 3:
                retval[7] = i
            elif len(i) == 4:
                retval[4] = i
            elif len(i) == 7:
                retval[8] = i
            else:
                remainder.append(i)
    return (retval, remainder)

def get069(arr, mapping):
    newList = []
    remainder = []
    for i in arr:
        if len(i) == 6:
            newList.append(i)
        else:
            remainder.append(i)
    strippedMap = removeDuplicateLetters(newList)    
    for i in strippedMap:
        if strippedMap[i][0] in mapping[4] and strippedMap[i][1] in mapping[4]:
            nine = i
        elif strippedMap[i][0] in mapping[1] or strippedMap[i][1] in mapping[1]:
            zero = i
        else:
            six = i
    return (nine, zero, six, remainder)

def get352(arr, mapping):
    strippedMap = removeDuplicateLetters(arr)    
    for i in strippedMap:
        if strippedMap[i][0] in mapping[1] and strippedMap[i][1] in mapping[1]:
            three = i
        elif strippedMap[i][0] in mapping[4] and strippedMap[i][1] in mapping[4]:
            five = i
        else:
            two = i
    return (three, five, two)

def removeDuplicateLetters(arr):
    mapping = {}
    for i in arr:
        mapping[i] = i
    
    keys = list(mapping.keys())
    for letter in keys[0]:
        if letter in keys[1] and letter in keys[2]:
            for entry in mapping:
                mapping[entry] = mapping[entry].replace(letter, '')
    return mapping
    
def main(): 
    with open('input') as f:
        lines = f.readlines()
        
    count = 0
    for line in lines:
        temp = line.split('|')
        inputs = [i.strip() for i in temp[0].split()]
        outputs = [i.strip() for i in temp[1].split()]
        mapping, inputs  = get1478(inputs)
        nine, zero, six, inputs = get069(inputs, mapping)
        mapping[9] = nine
        mapping[0] = zero
        mapping[6] = six
        three, five, two = get352(inputs, mapping)
        mapping[3] = three
        mapping[5] = five
        mapping[2] = two

        decoded = ''
        for output in outputs:
            for i in mapping:
                if sorted(output) == sorted(mapping[i]):
                    decoded += str(i)
        count += int(decoded)

    print(count)    
    


    
    
if __name__ == '__main__':
    sys.exit(main())
