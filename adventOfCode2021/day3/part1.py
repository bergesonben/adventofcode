with open('input') as f:
    lines = f.readlines()
    binaries = []
    for line in lines:
        binaries.append([int(c) for c in line.strip()])
    # print("binaries: " + binaries)
    mostCommonBits = []    
    leastCommonBits = []
    for i, bit in enumerate(binaries[0]):
        # print("i: " + str(i) + "; bit: " + str(bit))
        zeroes = 0
        ones = 0
        for bits in binaries:
            if bits[i] == 0:
                # print("adding a zero")
                zeroes += 1
            if bits[i] == 1:
                # print("adding a one")
                ones += 1        
        if zeroes > ones:
            mostCommonBits.append(0)   
            leastCommonBits.append(1)
        else:
            mostCommonBits.append(1)
            leastCommonBits.append(0) 

    gammaStr = ""    
    for bit in mostCommonBits:
        gammaStr += str(bit)
    gamma = int(gammaStr, 2)
    epsilonStr = ""
    for bit in leastCommonBits:
        epsilonStr += str(bit)
    epsilon = int(epsilonStr, 2)
    print("gamma: " + str(gamma) + "; epsilon: " + str(epsilon) + "; result: " + str(gamma * epsilon))
    
    




