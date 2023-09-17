import importlib
import random
def putShipOnMap(shipCoor, pMap):
    '''
    Util func to put 2's into player maps 
    '''
    # Assume shipCoor
    flatAllShipCoor = [item for sublist in shipCoor for item in sublist]
    for shipPos in flatAllShipCoor:
        shipPosX = shipPos[0]
        shipPosY = shipPos[1]
        pMap[shipPosX][shipPosY] = 2
    return pMap

def convertIntToMapIndex(int1, mapRow, mapCol):
    '''
    Use modullo and remainder to get map indexes. E.g.
    0 => 0,0 
    1 => 0,1 
    54 => 5,4
    99 => 9,9
    '''
    # 
    return (int1 // mapCol %mapRow , int1 % mapCol)

def convertMapIndToInt(index, mapRow, mapCol):
    '''
    Convert Map index to int. Eg.
    0,0 => 0
    0,1 => 1 
    9,9 => 99
    '''
    col = mapCol
    return (index[0] * mapRow) + index[1]



'''
================
file directories
================
'''
p1Script = "Battleship"
p2Script = "EnemyAi"

#dynamically import the module
p1 = importlib.import_module(p1Script)
p2 = importlib.import_module(p2Script)

shipSizeArr = [5,3,3,2,2]  # Change arr for more ships or diff ship sizes 
mapRows = 10 
mapCols = 10

yourHp = sum(shipSizeArr)   # 1 five block, 2 three block, 2 two block
enemyHp = sum(shipSizeArr)    
round = 1 
p1Storage = []
p2Storage = []


 # -------------------------------------------------------------- #
    #               Ship Positions/Coordinates                       #
    # -------------------------------------------------------------- #
    # Modify at your own risk ^.^
    # store every index/coord that the ship is covering, e.g. [(1,3), (1,4),(1,5)] for a ship of len 3. Each Coordinate must be 0-9. ([0-9], [0-9]).  
p1ShipPos = [[(3,1), (4,1),(5,1)], 
                [(2,1),(2,2),(2,3),(2,4),(2,5)], 
                [(7,7),(8,7)] , 
                [(0,9), (1,9), (2,9)], 
                [(5,9), (6,9)]]
# Coordinates on the board:
#           [[(2, 4), (2, 5), (2, 6)],
#           [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)], 
#           [(8, 8), (8, 9)], 
#           [(10, 1), (10, 2), (10, 3)], 
#           [(10, 6), (10, 7)]]

p2ShipPos = [[(3,1), (4,1),(5,1)], 
                [(2,1),(2,2),(2,3),(2,4),(2,5)], 
                [(7,7),(8,7)] , 
                [(0,9), (1,9), (2,9)], 
                [(5,9), (6,9)]]
# Coordinates on the board:
#           [[(4, 2), (5, 2), (6, 2)],
#           [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], 
#           [(8, 8), (9, 8)], 
#           [(1, 10), (2, 10), (3, 10)], 
#           [(6, 10), (7, 10)]]

assert len(p1ShipPos) == len(shipSizeArr) and len(p2ShipPos) == len(shipSizeArr), "Number of ships and Number of ShipPos coords must be consistent"

# We ain't checking too much so be careful of what you change :) -Author 
# -------------------------------------------------------------- #
#               Ship Positions/Coordinates                       #
# -------------------------------------------------------------- #

print (p1ShipPos)
print(p2ShipPos)
yourMap = putShipOnMap(p1ShipPos, [[0 for _ in range(mapRows)] for _ in range(mapCols)])
enemyMap = putShipOnMap(p2ShipPos, [[0 for _ in range(mapRows)] for _ in range(mapCols)])
yourValidBomb = [i for i in range(mapRows*mapCols)]   # [0,..., Row*Col-1], every int is an index 
enemyValidBomb = [i for i in range(mapRows*mapCols)]
p1ShotSeq = []
p2ShotSeq = []
p1Hit = []
p2Hit = []
p1PrevHit = False
p2PrevHit = False 

while yourHp > 0 or enemyHp > 0:        
    
    #-------------------------------------#
    #               Player 1              # 
    #-------------------------------------#

    # Assume we storing every coord a ship is covering 
    p1Bomb,p1Storage = p1.ShipLogic(round, yourMap, yourHp, enemyHp, p1ShotSeq, p1PrevHit,p1Storage)
    # convert coord from [1-10] to [0-9]
    bombX = p1Bomb[0]-1
    bombY = p1Bomb[1]-1

    if enemyMap[bombX][bombY] == 1 or enemyMap[bombX][bombY] == -1:
        # ShipLogic returns a coord that has been hit/chosen
        randValidBombIndex = random.randint(0,len(yourValidBomb)-1)  # Get index of valid coord
        randValidBombInt = yourValidBomb[randValidBombIndex]         # Get valid coord in Int form 
        randValidCoord = convertIntToMapIndex(randValidBombInt, mapRows, mapCols) # convert Int to map index 
        # New BombX, BombY
        bombX = randValidCoord[0]
        bombY = randValidCoord[1]
        # new p1Bomb from new XY 
        p1Bomb = [bombX+1, bombY+1]

    # p1Bomb is valid from this point on, p1Bomb is corrected or valid from the start 
    if enemyMap[bombX][bombY] == 2:
        p1PrevHit = True
        enemyMap[bombX][bombY] = -1
        round += 1 
        enemyHp -= 1
        p1ShotSeq.append(p1Bomb)  # append shot 
        p1Hit.append(1)           # util for front end to check if bomb hit  
        yourValidBomb.remove(convertMapIndToInt((bombX,bombY), mapRows, mapCols))  # remove coord (in Integer form) from valid moves arr
        if enemyHp == 0:
            break
    
    # Missed bomb 
    elif enemyMap[bombX][bombY] == 0:
        p1PrevHit = False
        enemyMap[bombX][bombY] = 1
        p1ShotSeq.append(p1Bomb)
        p1Hit.append(0)             # bomb no hit 
        yourValidBomb.remove(convertMapIndToInt((bombX,bombY), mapRows, mapCols))  # still remove coord (in Integer form) from valid moves arr

    #-------------------------------------#
    #               Player 2              # 
    #-------------------------------------#
    
    p2Bomb, p2Storage = p2.ShipLogic(round, enemyMap, enemyHp, yourHp, p2ShotSeq, p2PrevHit, p2Storage)
    # convert coord from [1-10] to [0-9]
    bombX = p2Bomb[0]-1
    bombY = p2Bomb[1]-1

    if yourMap[bombX][bombY] == 1 or yourMap[bombX][bombY] == -1:
        # ShipLogic returns a coord that has been hit/chosen
        randValidBombIndex = random.randint(0,len(enemyValidBomb)-1)        # Get index of valid coord
        randValidBombInt = enemyValidBomb[randValidBombIndex]               # Get valid coord in Int form 
        randValidCoord = convertIntToMapIndex(randValidBombInt, mapRows, mapCols) # convert Int to map index 
        # New BombX, BombY
        bombX = randValidCoord[0]
        bombY = randValidCoord[1]
        # new p2Bomb from new XY 
        p2Bomb = [bombX+1, bombY+1]

    # p2Bomb is valid from this point on, p2Bomb is corrected or valid from the start 
    if yourMap[bombX][bombY] == 2:
        p2PrevHit = True 
        yourMap[bombX][bombY] = -1
        round += 1 
        yourHp -= 1
        p2ShotSeq.append(p2Bomb)    # append shot 
        p2Hit.append(1)             # util for front end to check if bomb hit  
        enemyValidBomb.remove(convertMapIndToInt((bombX,bombY), mapRows, mapCols))  # remove coord (in Integer form) from valid moves arr
        if yourHp == 0:
            break
        
    elif yourMap[bombX][bombY] == 0:
        p2PrevHit = False 
        yourMap[bombX][bombY] = 1
        p2ShotSeq.append(p2Bomb)
        p2Hit.append(0)         # bomb no hit 
        enemyValidBomb.remove(convertMapIndToInt((bombX,bombY), mapRows, mapCols)) # still remove coord (in Integer form) from valid moves arr




'''
==========================================================

                PRINT INFORMATION 
                feel free to edit
                
==========================================================
'''
print("\n\n\n============battle stat============") 
if yourHp > 0: 
    print("YOU WIN")

if enemyHp > 0:
    print("YOU LOSE")
print("Your HP: ",yourHp)
print("Enemy HP: ",enemyHp)
print("Your shots: \n",yourMap,"\n")

print("Enemy shots: \n",p2ShotSeq,"\n")