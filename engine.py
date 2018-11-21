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

def place(board, base, fixed, size, orientation, occupied):
    for i in range(size):
        if orientation == 'vertical':
            occupied.append((base + i, fixed))
            board[base + i][fixed] = 'o'
        elif orientation == 'horizontal':
            occupied.append((fixed, base + i))
            board[fixed][base + i] = 'o'

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

def hitcheck(board, coordinates, occupied):
    if coordinates in occupied:
        board[coordinates[0]][coordinates[1]] = 'x'
        occupied.remove(coordinates)

if __name__ == '__main__':
    board = grid()
    occupied = []
    for i in ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer'):
        while True:
            print(board)
            print(occupied)
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
            
        
    
    
