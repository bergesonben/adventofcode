REQUIRED_FIELDS = {'byr','iyr','eyr','hgt','hcl','ecl','pid'}
VALID_EYE_COLORS = {'amb','blu','brn','gry','grn','hzl','oth'}

def isValidYear(name, value):    
    if len(value) != 4:
        return False
    if name == 'byr':
        return 1920 <= int(value) <= 2002
    elif name == 'iyr':
        return 2010 <= int(value) <= 2020
    elif name == 'eyr':
        return 2020 <= int(value) <= 2030

def isHGTValid(value):
    if len(value) < 3:
        return False
    unit = value[-2:]
    if unit == 'cm':
        return 150 <= int(value[:-2]) <= 193
    elif unit == 'in':
        return 59 <= int(value[:-2]) <= 76
    else:
        return False

def isHCLValid(value):
    if len(value) != 7:
        return False
    if value[0] != '#':
        return False
    for c in value[1:]:
        if not c in '0123456789abcdef':
            return False
    return True

def isFieldValid(name, value):
    value = value.strip() 
    if name == 'byr' or name == 'iyr' or name == 'eyr':
        return isValidYear(name, value)
    elif name == 'hgt':
        return isHGTValid(value)
    elif name == 'hcl':
        return isHCLValid(value)
    elif name == 'ecl':
        return value in VALID_EYE_COLORS
    elif name == 'pid':
        return len(value) == 9 and value.isnumeric()
    elif name == 'cid':
        return True
    else:
        return False

def isPassportValid(fields):
    fieldsDict = {}
    for field in fields:
        foo = field.split(':')
        fieldsDict[foo[0]] = foo[1]

    fieldNames = set(fieldsDict.keys())
    if REQUIRED_FIELDS.intersection(fieldNames) != REQUIRED_FIELDS:
        return False    

    for fieldName, fieldValue in fieldsDict.items():
        if not isFieldValid(fieldName, fieldValue):
            return False
    return True

def main(input):
    with open(input) as f:
        lines = f.readlines()

    fieldsSoFar = set()
    validCount = 0
    for line in lines:
        if line.isspace():
            if isPassportValid(fieldsSoFar):
                validCount += 1
            fieldsSoFar = set()
            
        for entry in line.strip().split():
            fieldsSoFar.add(entry)
    
    if isPassportValid(fieldsSoFar):
        validCount += 1

    print(validCount)
   
