class PasswordRequirement:
    def __init__(self, pos1, pos2, letter):
        self.pos1 = pos1-1
        self.pos2 = pos2-1
        self.letter = letter
    
    def isValid(self, password):
        return (password[self.pos1] == self.letter) != (password[self.pos2] == self.letter)

def main(input):
    with open(input) as f:
        lines = f.readlines()

    numValid = 0
    for line in lines:
        line = line.strip().split()
        reqNums = line[0].split('-')
        reqLetter = line[1].replace(':','')
        requirement = PasswordRequirement(int(reqNums[0]), int(reqNums[1]), reqLetter)
        password = line[2]
        if requirement.isValid(password):
            numValid += 1
    
    print(numValid)

