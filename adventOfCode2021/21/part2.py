import sys
import json

DEBUG = True
USE_CACHE = False
IS_TEST = True
CACHE_FILE = None
CACHE_FILE_TEST = '/home/benjamin/Documents/adventOfCode2021/21/test_cache'
CACHE_FILE_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/test_cache2'
TEST_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/test'
ACTUAL_INPUT = '/home/benjamin/Documents/adventOfCode2021/21/input'
SCORE_MAX = 21
    
POSSIBILITIES = {
    3:1,
    4:3,
    5:6,
    6:7,
    7:6,
    8:3,
    9:1
}

class Universe:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
    
    def fromTuple(tuple):
        player1Tuple = tuple[0]
        player2Tuple = tuple[1]
        player1 = Player(player1Tuple[0], player1Tuple[1])
        player2 = Player(player2Tuple[0], player2Tuple[1])
        return Universe(player1, player2)
        
    def tuple(self):
        return (self.player1.tuple(), self.player2.tuple())
    
    def __str__(self):
        return 'player1 pos:' + str(self.player1.pos) + ',score:' + str(self.player1.score) + '\t\tplayer2 pos:' + str(self.player2.pos) + ',score:' + str(self.player2.score)

class Player:
    posMax = 10
    def __init__(self, pos, score):
        self.pos = pos 
        self.score = score
    
    def rollOver(num):        
        num = num % Player.posMax
        num = 10 if num == 0 else num
        return num    
    
    def tuple(self):
        return (self.pos, self.score)

def move(universes, player1Turn):
    newUniverses = {}       
    won = 0 
    for universeTuple, count in universes.items():
        universe = Universe.fromTuple(universeTuple)
        player = universe.player1 if player1Turn else universe.player2
        otherPlayer = universe.player2 if player1Turn else universe.player1
        for possibility in POSSIBILITIES:
            newPos = Player.rollOver(player.pos + possibility)
            newScore = player.score + newPos
            if newScore >= SCORE_MAX:  
                won += POSSIBILITIES[possibility] * count                                       
                continue
            newPlayer = Player(newPos, newScore)
            if player1Turn:
                newUniverse = Universe(newPlayer, otherPlayer)
            else:
                newUniverse = Universe(otherPlayer, newPlayer)
            newUniverseTuple = newUniverse.tuple()
            if newUniverseTuple in newUniverses:
                newUniverses[newUniverseTuple] += POSSIBILITIES[possibility] * count
            else:
                newUniverses[newUniverseTuple] = POSSIBILITIES[possibility] * count
    return (newUniverses, won)

def main(): 
    global DEBUG, USE_CACHE, IS_TEST, CACHE_FILE
    DEBUG = True if '-d' in sys.argv else False
    USE_CACHE = True if '-c' in sys.argv else False
    IS_TEST =  True if '-t' in sys.argv else False
    CACHE_FILE = CACHE_FILE_TEST if IS_TEST else CACHE_FILE_INPUT
  
    with open(TEST_INPUT if IS_TEST else ACTUAL_INPUT) as f:
        lines = f.readlines()  
    
    player1 = Player(int(lines[0].split()[-1]), 0)
    player2 = Player(int(lines[1].split()[-1]), 0)
    player1Turn = True
    round = 1
    universes = {
        Universe(player1, player2).tuple(): 1
    }
    p1NumWins = 0
    p2NumWins = 0
    while universes:    
        roundPrint = '==========round ' + str(round) + ': '
        if player1Turn:
            roundPrint += 'player1'
        else:
            roundPrint += 'player2'
            round += 1
        roundPrint += '==========='
        # print(roundPrint)
        universes, newWins = move(universes, player1Turn)
        if player1Turn:
            p1NumWins += newWins
        else:
            p2NumWins += newWins
        player1Turn = not player1Turn        
        
    
    print('player1: ' + str(p1NumWins))
    print('player2: ' + str(p2NumWins))
   





    

if __name__ == '__main__':
    sys.exit(main())

