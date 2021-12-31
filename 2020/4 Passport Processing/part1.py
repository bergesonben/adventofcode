REQUIRED_FIELDS = {'byr','iyr','eyr','hgt','hcl','ecl','pid'}

def main(input):
    with open(input) as f:
        lines = f.readlines()

    fieldsSoFar = set()
    validCount = 0
    for line in lines:
        if line.isspace():
            if REQUIRED_FIELDS.intersection(fieldsSoFar) == REQUIRED_FIELDS:
                validCount += 1
            fieldsSoFar = set()
            
        for entry in line.strip().split():
            fieldsSoFar.add(entry.split(':')[0])
    
    if REQUIRED_FIELDS.intersection(fieldsSoFar) == REQUIRED_FIELDS:
        validCount += 1

    print(validCount)
   
