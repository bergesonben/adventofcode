from itertools import combinations

def main(input):
    with open(input) as f:
        lines = f.readlines()

    lines = [int(i) for i in lines]
    
    combos = combinations(lines, 2)
    for combo in combos:
        if combo[0] + combo[1] == 2020:
            answer = combo[0] * combo[1] 
            break
    
    if answer is None:
        print('no answer found')
    else:
        print(answer)

