"""
Possible states of a grid
* unoccupied - '00'
* occupied with
   knight N
   rook R
   queen Q
   bishop B
   king K 
   pawn P
* colour - b, w
"""

game_grid = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
             ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'], 
             ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

game_grid = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
             ['bP', 'bP', 'bP', '00', 'bP', 'bP', 'bP', 'bP'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['00', '00', '00', 'bQ', '00', '00', '00', '00'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['00', '00', '00', '00', '00', '00', '00', '00'], 
             ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'], 
             ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

def print_grid(game_grid):
    q = 0
    for i in range(1,20):
        
        if i == 1 or i == 19: #column numbering
            print("    ",end='')
            for j in range(1,9):
                print("   ",j-1," ",end="")
            print()
            
        elif i == 2 or i == 18: #equals
            print("    ",end='')
            print("="*57)
            
        elif i%2 == 0: #separators of boxes
            print("   ",end=' ')
            print("|",end='')
            print("------|"*8)
            
        else:
            print(" ",q,end=' ')
            for j in range(0,8): #boxes
                print("| ",game_grid[q][j]," ",end="")
            print("|",q)
            q = q + 1

# [N, NE, E, SE, S, SW, W, NW]
# Except bishop
range_of_motion = {
     'K':[1, 0, 1, 0, 1, 0, 1, 0],
     'Q':['inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf', 'inf'],
     'R':['inf',0, 'inf', 0, 'inf', 0, 'inf', 0],
     'B':[0, 'inf', 0, 'inf', 0, 'inf', 0, 'inf'],
     'wP':[1, 0, 0, 0, 0, 0, 0, 0],
     'bP':[0, 0, 0, 0, 1, 0, 0, 0]
}

def moveValid(startx, starty, endx, endy, player):

    start_piece = game_grid[startx][starty]
    start_piece_colour = start_piece[0]

    if ((not positionIsUnoccupied(startx, starty) or start_piece_colour == player) and (canGo(endx, endy, startx, starty) or not positionIsUnoccupied(endx, endy) and canAttack(endx, endy, startx, starty))):
        return True
    return False


# Given non empty start, a target, it determines whether the target lies on possible paths of the start piece
def canGo(targetX, targetY, startX, startY):


    start_piece = game_grid[startX][startY]

    if start_piece[1] == 'N': #For horse, same logic as canAttack
        for jump in horse_jump_adders:
            jump_endX, jump_endY = startX + jump[0], startY + jump[1]

            if isEqualCoordinates(targetX, targetY, jump_endX, jump_endY):
                return True
        else:
            return False
    else:
        path_li = generatePossiblePaths(startX, startY)
        for i in range(8):
            path_space = path_li[i]

            xDir = direction_adders[i][0]
            yDir = direction_adders[i][1]

            for j in range(1,path_space+1):
                if isEqualCoordinates(targetX, targetY, startX + j * xDir, startY + j * yDir):
                    return True
        else:
            return False

# Given non empty start, non-empty target can start piece attack the target in a move
# Checks whether an opponent piece:
# -- (for horse) lies at the jump points of the horse
# -- (for pawn) lies at the end+1 point of possible path OR lies diagonally wrt pawn
# -- (for all other pieces) lies at the end+1 point of the possible paths of the piece
def canAttack(targetX, targetY, startX, startY):

    start_piece = game_grid[startX][startY]
    end_piece = game_grid[targetX][targetY]

    if oppositeColours(start_piece, end_piece):
        if start_piece[1] == 'N':
            for jump in horse_jump_adders:
                jump_endX, jump_endY = startX + jump[0], startY + jump[1]

                if isEqualCoordinates(targetX, targetY, jump_endX, jump_endY):
                    return True
            else:
                return False
        else:
            path_li = generatePossiblePaths(startX, startY)

            if start_piece[1] == 'wP':
                if isEqualCoordinates(targetX, targetY, startX-1, startY+1) or isEqualCoordinates(targetX, targetY, startX-1, startY-1):
                    return True
            elif start_piece[1] == 'bP':
                if isEqualCoordinates(targetX, targetY, startX+1, startY+1) or isEqualCoordinates(targetX, targetY, startX+1, startY-1):
                    return True

            for i in range(8):
                path_space = path_li[i]

                xDir = direction_adders[i][0]
                yDir = direction_adders[i][1]

                path_endX = startX + xDir * (path_space + 1)
                path_endY = startY + yDir * (path_space + 1)

                if isEqualCoordinates(targetX, targetY, path_endX, path_endY):
                    return True

            else:
                return False

    return False

def isEqualCoordinates(x1,y1,x2,y2):
    if (x1 == x2) and (y1 == y2):
        return True
    return False

def oppositeColours(piece1, piece2):
    if (piece1[0] == 'w' and piece2[0] == 'b') or (piece1[0] == 'b' and piece2[0] == 'w'):
        return True
    return False

def isInsideGrid(x,y):
    if x > 7 or x < 0 or y > 7 or y < 0:
        return False
    return True

def positionIsUnoccupied(x,y):
    if game_grid[x][y] == '00':
        return True
    return False

# def addCoordinates(A, B):
#     return [A[0] + B[0], A[1] + B[1]]

direction_adders = [(-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (1,-1)]
horse_jump_adders = [(-2,1), (-1,2), (1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1)]

def makePossiblePathsGrid(startx, starty, path, game_grid):
    for i in range(8):
        path_space = path[i]

        xDir = direction_adders[i][0]
        yDir = direction_adders[i][1]

        nextx, nexty = startx + xDir, starty + yDir
        while path_space > 0:
            game_grid[nextx][nexty] = "##"
            nextx += xDir
            nexty += yDir
            path_space -= 1

    return game_grid

# if piece[1] == 'N':
#     for jump in horse_jump_adders:
#         jump_endX, jump_endY = startx + jump[0], starty + jump[1]
#         if positionIsUnoccupied(jump_endX, jump_endY):
#             path_coordinates.append((jump_endX, jump_endY))
def generatePossiblePaths(startx, starty):
    piece = game_grid[startx][starty]
    path = [0]*8
    if piece[1] != 'P':
        piece = piece[1]

    for i in range(8):
        remaining_range = range_of_motion[piece][i]

        xDir = direction_adders[i][0]
        yDir = direction_adders[i][1]

        nextx, nexty = startx + xDir, starty + yDir

        inf_flag = 0
        if remaining_range == 'inf':
            inf_flag = 1
            remaining_range = 2

        while isInsideGrid(nextx, nexty) and remaining_range > 0:
            if positionIsUnoccupied(nextx,nexty):
                if inf_flag == 1:
                    remaining_range = 2

                path[i] += 1;
                remaining_range -= 1;

                nextx += xDir
                nexty += yDir

            else:
                break

    return path

while True:
    print_grid(game_grid)
    startx, starty, targetx, targety = list(map(int, input("Enter: ").split()))

    print(moveValid(startx, starty, targetx, targety,'b'))
    if startx == -1:
        break

# startx, starty = 1, 1
# piece = game_grid[startx][starty]

# targetx, targety = 2, 1
# tartget_piece = game_grid[targetx][targety]

# print_grid(game_grid)
# path_coordinates = generatePossiblePaths(startx , starty)
# print(moveValid(startx, starty, targetx, targety,'w'))
# print(canGo(targetx,targety, startx, starty))
# print_grid(makePossiblePathsGrid(startx, starty, path_coordinates, game_grid))
