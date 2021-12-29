import sys
import collections

DEBUG = True
USE_CACHE = False
IS_TEST = True
CACHE_FILE = None
CACHE_FILE_TEST = '/home/benjamin/Documents/adventOfCode2021/21/test_cache'
CACHE_FILE_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/test_cache2'
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/input'

class DeterministicDice:
    max = 100
    def __init__(self):
        self.next = 1

    def roll(self):
        answer = [DeterministicDice.rollOver(self.next), DeterministicDice.rollOver(self.next + 1), DeterministicDice.rollOver(self.next + 2)]
        self.next = DeterministicDice.rollOver(self.next + 3)
        return answer
    
    def rollOver(num):
        return num if num <= DeterministicDice.max else num - DeterministicDice.max
    
class Player:
    posMax = 10
    def __init__(self, startingPos):
        self.score = 0
        self.pos = startingPos
    
    def move(self, movesCount):
        self.pos = Player.rollOver(self.pos + movesCount)
        self.score += self.pos
    
    def rollOver(num):        
        while num > Player.posMax:
            num = num - Player.posMax
        return num    

def getLoserOrNone(player1, player2):
    if player1.score >= 1000 and player2.score >= 1000:
        raise Exception('both players won')
    
    if player1.score >= 1000: return player2
    elif player2.score >= 1000: return player1
    else: return

def main(): 
    global DEBUG, USE_CACHE, IS_TEST, CACHE_FILE
    DEBUG = True if '-d' in sys.argv else False
    USE_CACHE = True if '-c' in sys.argv else False
    IS_TEST =  True if '-t' in sys.argv else False
    CACHE_FILE = CACHE_FILE_TEST if IS_TEST else CACHE_FILE_INPUT
  
    with open(TEST_INPUT if IS_TEST else ACTUAL_INPUT) as f:
        lines = f.readlines()  
    
    player1 = Player(int(lines[0].split()[-1]))
    player2 = Player(int(lines[1].split()[-1]))
    player1Turn = True
    dice = DeterministicDice()
    diceRolls = 0
    loser = None
    while loser is None:
        diceRolls += 3
        playerToGo = player1 if player1Turn else player2
        totolMove = sum(dice.roll())
        playerToGo.move(totolMove)
        player1Turn = not player1Turn
        loser = getLoserOrNone(player1, player2)
    
    print('loser score: ' + str(loser.score))
    print('dice rolls: ' + str(diceRolls))
    answer = loser.score * diceRolls
    print(answer)





    

if __name__ == '__main__':
    sys.exit(main())

