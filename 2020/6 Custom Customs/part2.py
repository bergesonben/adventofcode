import string

class Group:
    def __init__(self, answers):
        self.answers = answers

    def getNumAnswers(self):
        return len(self.answers)

def main(input):
    with open(input) as f:
        lines = f.readlines()

    soFar = set(list(string.ascii_lowercase))
    groups = []
    for line in lines:
        if line.isspace():
            groups.append(Group(soFar))
            soFar = set(list(string.ascii_lowercase))
        else:
            person = set()
            for c in line.strip():
                person.add(c)
            soFar = soFar.intersection(person)
        
    groups.append(Group(soFar))

    answer = sum(group.getNumAnswers() for group in groups)
    print(answer)