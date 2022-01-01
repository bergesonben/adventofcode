class Group:
    def __init__(self, answers):
        self.answers = answers

    def getNumAnswers(self):
        return len(self.answers)

def main(input):
    with open(input) as f:
        lines = f.readlines()

    soFar = set()
    groups = []
    for line in lines:
        if line.isspace():
            groups.append(Group(soFar))
            soFar = set()
        for c in line.strip():
            soFar.add(c)
    groups.append(Group(soFar))

    answer = sum(group.getNumAnswers() for group in groups)
    print(answer)