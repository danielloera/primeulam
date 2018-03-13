from graphics import *

UP = "up"
LEFT = "left"
DOWN = "down"
RIGHT = "right"

next_movement = {
            UP: LEFT,
            LEFT: DOWN,
            DOWN: RIGHT,
            RIGHT: UP
                            }

def in_bounds(x, y, size):
    return x >= 0 and x < size and y >= 0 and y < size

def neighbor(curr_movement, x, y, board):
    if curr_movement == UP:
        return board[x][y - 1]
    if curr_movement == LEFT:
        return board[x + 1][y]
    if curr_movement == DOWN:
        return board[x][y + 1]
    return board[x - 1][y]

def update(curr_movement, x, y):
    if curr_movement == UP:
        return x - 1, y
    if curr_movement == LEFT:
        return x, y - 1
    if curr_movement == DOWN:
        return x + 1, y
    return x, y + 1

def spiralize(board):
    size = len(board)
    center = size // 2
    x, y = center, center
    num = 1
    board[x][y] = num
    y += 1
    num += 1
    movement = "up"
    while in_bounds(x, y, size):
        if neighbor(movement, x, y, board) is not None:
            board[x][y] = num
            x, y = update(movement, x, y)
            num += 1
        else:
            movement = next_movement[movement]

# Thanks to "dawg" from stackoverflow
def is_prime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n%f == 0: return False
    if n%(f+2) == 0: return False
    f +=6
  return True   

if len(sys.argv) < 2:
    raise Exception("Please enter the spiral size")

size = int(sys.argv[1])

if size % 2 != 1:
    raise Exception("Please enter a odd number")

board = [[None for i in range(size)] for j in range(size)]

spiralize(board)
win = GraphWin("Prime Ulam Spiral (size {}) ".format(size), size, size)
win.setBackground("black")

for i in range(len(board)):
    for j in range(len(board)):
        if is_prime(board[i][j]):
            win.plot(i, j, "white")

win.getMouse()
win.close()
