
def parseRule(line):
    a = line.split('contain')
    outterBag = a[0].replace('bags','').strip()
    innerBags = set()
    if 'no other bags.' in a[1]:
        return []
    bagsRaw = [i.strip() for i in a[1].split(',')]
    for bagRaw in bagsRaw[:-1]:
        count = int(bagRaw[0])
        innerBags.add(bagRaw[1:].replace('bag' if count == 1 else 'bags', '').strip())
    count = int(bagsRaw[-1][0])
    innerBags.add(bagsRaw[-1][1:-1].replace('bag' if count == 1 else 'bags', '').strip())        

    return [(innerBag, {outterBag}) for innerBag in innerBags]

def main(input):
    with open(input) as f:
        lines = f.readlines()

    bags = {}
    for line in lines:
        rule = parseRule(line)
        for innerBag, outterBag in rule:
            if innerBag in bags:
                bags[innerBag] = bags[innerBag].union(outterBag)
            else:
                bags[innerBag] = outterBag
    
    bagsToCheck = {'shiny gold'}
    checkedBags = set()
    validBags = set()
    while len(bagsToCheck) != 0:
        currBag = bagsToCheck.pop()
        checkedBags.add(currBag)
        if currBag in bags:
            validBags = validBags.union(bags[currBag])
            bagsToCheck = bagsToCheck.union(set(b for b in bags[currBag] if not b in checkedBags))
    print(len(validBags))
