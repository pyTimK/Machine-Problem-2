import random
from GameObjects import GamePiece

def grid():
    #returns a 10x10 grid
    board = [ ['.' for _ in range(10)] for _ in range(10)]
    return board

def shipcheck(base, fixed, size, board, occupied):
    if base + size > len(board):
        #checks if the ship fits the board
        return False
    for i in range(size):
        #uses coordinates to check if ship intersects another ship
        if orientation == 'vertical':
            if (base + i, fixed) in occupied:
                return False
        elif orientation == 'horizontal':
            if (fixed, base + i) in occupied:
                return False
    return True

def ai_shipcheck(base, fixed, size, ai_board, ai_occupied):
    if base + size > len(ai_board):
        #checks if the ship fits the board
        return False
    for i in range(size):
        #uses coordinates to check if ship intersects another ship
        if orientation == 'vertical':
            if (base + i, fixed) in ai_occupied:
                return False
        elif orientation == 'horizontal':
            if (fixed, base + i) in ai_occupied:
                return False
    return True

def place(board, base, fixed, size, orientation, occupied):
    for i in range(size):
        if orientation == 'vertical':
            occupied.append((base + i, fixed))
            board[base + i][fixed] = 'o'
        elif orientation == 'horizontal':
            occupied.append((fixed, base + i))
            board[fixed][base + i] = 'o'

def ai_place(ai_board, base, fixed, size, orientation, ai_occupied):
    for i in range(size):
        if orientation == 'vertical':
            ai_occupied.append((base + i, fixed))
            ai_board[base + i][fixed] = 'o'
        elif orientation == 'horizontal':
            ai_occupied.append((fixed, base + i))
            ai_board[fixed][base + i] = 'o'

def shipset(board, coordinates, orientation, ship):
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    if shipcheck(base, fixed, size, board, occupied):
        place(board, base, fixed, size, orientation, occupied)
        return True
    else:
        return 'Please try again.'

def ai_shipset(ai_board, coordinates, orientation, ship):
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    if ai_shipcheck(base, fixed, size, ai_board, ai_occupied):
        ai_place(ai_board, base, fixed, size, orientation, ai_occupied)
        return True

def hitcheck(board, coordinates, occupied):
    if coordinates in occupied:
        board[coordinates[0]][coordinates[1]] = 'x'
        ai_occupied.remove(coordinates)

#modified version of hitcheck
def ai_hitcheck(board, coordinates, occupied):
    board.attack_positions.append((coordinates[1],coordinates[0])) ###
    if coordinates in occupied:
        board.grid[coordinates[0]][coordinates[1]] = 'x'
        for i in range(len(occupied)):
            if occupied[i] == coordinates:
                occupied[i] = 'h'
        return True
    else:
        board.grid[coordinates[0]][coordinates[1]] = 'm'
        return False

#chooses logical coordinates
#if the attempts to choose a logical coordinate exceeds 10
#it will choose any coordinate
def ai_coordinates(player_ships, board):
    attempt = 0
    while True:
        attempt += 1
        if attempt == 10:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                coordinates = (x, y)
                if board.grid[x][y] == '.' or board.grid[x][y] == 'o':
                    return coordinates
        #x = int(input())
        #y = int(input())
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        coordinates = (x, y)
        if player_ships[-1] == 'destroyer':
            n = 2
        elif player_ships[-1] == 'submarine' or player_ships[-1] == 'cruiser':
            n = 3
        elif player_ships[-1] == 'battleship':
            n = 4
        elif player_ships[-1] == 'carrier':
            n = 5
        if board.grid[x][y] == '.' or board.grid[x][y] == 'o':
            counter1 = 1
            counter2 = 1
            for p in range(1, n):
                if x + n <= 9:
                    if board.grid[x + n][y] == '.' or board.grid[x + n][y] == 'o':
                        counter1 += 1
                if x - n >= 0:
                    if board.grid[x - n][y] == '.' or board.grid[x - n][y] == 'o':
                        counter1 += 1
                if y + n <= 9:
                    if board.grid[x][y + n] == '.' or board.grid[x][y + n] == 'o':
                        counter2 += 1
                if y - n >= 0:
                    if board.grid[x][y - n] == '.' or board.grid[x][y - n] == 'o':
                        counter2 += 1
            if counter1 == n or counter2 == n:
                break
    return coordinates

#checks if any of the player's ships has been destroyed
def check_destroyed(occupied, coordinates):
    if occupied[0] == 'h' and occupied[1] == 'h' and occupied[2] == 'h' and occupied[3] == 'h' and occupied[4] == 'h':
        print('Your carrier has been destroyed')
    if occupied[5] == 'h' and occupied[6] == 'h' and occupied[7] == 'h' and occupied[8] == 'h':
        print('Your battleship has been destroyed')
    if occupied[9] == 'h' and occupied[10] == 'h' and occupied[11] == 'h':
        print('Your cruiser has been destroyed')
    if occupied[12] == 'h' and occupied[13] == 'h' and occupied[14] == 'h':
        print('Your submarine has been destroyed')
    if occupied[15] == 'h' and occupied[16] == 'h':
        print('Your destroyer has been destroyed')

#makes a decision if the ai hits a ship
def ai_repeat(board, coordinates, result, decision, occupied):
    lock = 0
    x = coordinates[0]
    y = coordinates[1]
    while True:
        lock += 1
        if decision == 0:
            x += 1
            if x <= 9:
                break
            else:
                x -=1
                decision = 1
        elif decision == 1:
            x -= 1
            if x >= 0:
                break
            else:
                x += 1
                decision = 0
        elif decision == 2:
            y += 1
            if y <= 9:
                break
            else:
                y -= 1
                decision = 3
        elif decision == 3:
            y -= 1
            if y >= 0:
                break
            else:
                y += 1
                decision = 2
        coordinates = (x, y)
        result = ai_hitcheck(board, coordinates, occupied)
        if result == False:
            if decision == 0:
                decision = 1
            elif decision == 1:
                decision = 0
            elif decision == 2:
                decision = 3
            elif decision == 3:
                decision = 2
            break
    if lock == 1:
        decision = 4
    return decision

#checks if the ai has any possible move left
def no_moves(board):
    counter = 0
    for x in range(10):
        for y in range(10):
            if board.grid[x][y] == 'x' or board.grid[x][y] == 'm':
                counter += 1
    if counter == 100:
        return True
    else:
        return False

#what the ai does in its turn
def ai_hit(board, occupied, player_ships, previous):
    if no_moves(board) == False:
        decision = previous[0]
        coordinates = previous[1]
        if decision != 4:
            previous[0] = ai_repeat(board, coordinates, result, decision, occupied)
            return previous
        coordinates = ai_coordinates(player_ships, board)
        previous[1] = coordinates
        result = ai_hitcheck(board, coordinates, occupied)
        if result == True:
            decision = random.randint(0, 3)
            previous[0] = ai_repeat(board, coordinates, result, decision, occupied)
            return previous
    else:
        print('There are no possible moves left')


###ADDED BY TIM
def ship_unset(board, coordinates, orientation, ship):
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    for i in range(size):
        if orientation == 'vertical' and ((base + i, fixed) in occupied):
            occupied.remove((base + i, fixed))
            board[base + i][fixed] = '.'
        elif orientation == 'horizontal' and ((fixed, base + i) in occupied):
            occupied.remove((fixed, base + i))
            board[fixed][base + i] = '.'


def mouse_position_is_in(instance_name,x,y):
    if isinstance(instance_name, GamePiece):
        width=instance_name.image.width
        height=instance_name.image.height
        if instance_name.orientation=='vertical':
            width=instance_name.image.height
            height=instance_name.image.width

        if instance_name.sprite.x - width//2 <=x<=instance_name.sprite.x+width//2 and instance_name.sprite.y - height//2<=y<=instance_name.sprite.y+height//2:
            return True
        else:
            return False
    if instance_name.sprite.x<=x<=instance_name.sprite.x+instance_name.image.width and instance_name.sprite.y<=y<=instance_name.sprite.y+instance_name.image.height:
        return True
    return False

def ai_set_ships(ai_board,ai_ship_list):
    global orientation
    for ai_ship in ai_ship_list:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coordinates = (x, y)
            temp = random.randint(0, 1)
            
            if temp == 1:
                ai_ship.switch_orientation()
            orientation= ai_ship.orientation
            result = shipset(ai_board.grid, coordinates, ai_ship.orientation, ai_ship.name)
            if result == True:
                if ai_ship.orientation=='vertical':
                    ai_ship.sprite.x = ai_board.sprite.x+x*40+ai_ship.image.height//2
                    ai_ship.sprite.y = ai_board.sprite.y+(10-y)*40 - ai_ship.image.width//2
                else:
                    ai_ship.sprite.x = ai_board.sprite.x+x*40+ai_ship.image.width//2
                    ai_ship.sprite.y = ai_board.sprite.y+(10-y)*40 - ai_ship.image.height//2
                if ai_ship.orientation=='vertical':
                    for i in range(ai_ship.size):
                        ai_ship.coordinates.append((x,y+i))
                else:
                    for i in range(ai_ship.size):
                        ai_ship.coordinates.append((x+i,y))
                print(ai_ship.name)
                print(ai_ship.coordinates)
                for row in ai_board.grid:
                    print(row)
                print('')
                break



if __name__ == '__main__':
    #sets up ai board
    ai_board = grid()
    board = grid()
    ai_occupied = []
    occupied = []
    previous = [4, (0, 0)]
    player_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
    ai_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
    for i in ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer'):
        while True:
            print(ai_board)
            print(ai_occupied)
            print(i)
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coordinates = (x, y)
            temp = random.randint(0, 1)
            orientation = 'horizontal'
            if temp == 0:
                orientation = 'vertical'
            elif temp == 1:
                orientation = 'horizontal'
            result = ai_shipset(ai_board, coordinates, orientation, i)
            if result == True:
                break
            else:
                print(result)
        print(ai_board)
        print(ai_occupied)

    #sets up player board
    for i in ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer'):
        while True:
            print(i)
            x = int(input())
            y = int(input())
            coordinates = (x, y)
            orientation = input()
            result = shipset(board, coordinates, orientation, i)
            if result == True:
                break
            else:
                print(result)
        print(board)
        print(occupied)

    #ai test
    while input() == 'test':
        previous = ai_hit(board, occupied, player_ships, previous)
        check_destroyed(occupied, coordinates)
        print(board)
        print(occupied)
