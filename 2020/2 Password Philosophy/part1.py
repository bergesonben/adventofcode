from itertools import combinations
from typing import MappingView

class PasswordRequirement:
    def __init__(self, minimum, maximum, letter):
        self.min = minimum
        self.max = maximum
        self.letter = letter
    
    def isValid(self, password):
        return self.min <= password.count(self.letter) <= self.max

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

