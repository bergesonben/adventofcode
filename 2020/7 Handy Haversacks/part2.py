def parseRule(line):
    a = line.split('contain')
    outterBag = a[0].replace('bags','').strip()
    innerBags = []
    if 'no other bags.' in a[1]:
        return (outterBag, [])
    bagsRaw = [i.strip() for i in a[1].split(',')]
    for bagRaw in bagsRaw[:-1]:
        count = int(bagRaw[0])
        innerBags.append((count,bagRaw[1:].replace('bag' if count == 1 else 'bags', '').strip()))
    count = int(bagsRaw[-1][0])
    innerBags.append((count, bagsRaw[-1][1:-1].replace('bag' if count == 1 else 'bags', '').strip()))

    return (outterBag, innerBags)

def main(input):
    with open(input) as f:
        lines = f.readlines()

    bags = {}
    for line in lines:
        outterBag, innerBags = parseRule(line)        
        if outterBag in bags:
            bags[outterBag] += innerBags
        else:
            bags[outterBag] = innerBags

    bagsToCheck = [(1,'shiny gold')]
    numBags = -1
    while len(bagsToCheck) != 0:
        currBagAndCount = bagsToCheck.pop()
        if currBagAndCount[1] in bags:
            numBags += currBagAndCount[0]
            bagsToCheck += [(i[0]*currBagAndCount[0], i[1]) for i in bags[currBagAndCount[1]]]
    print(numBags)
