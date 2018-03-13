from graphics import *
import argparse

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

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
    x, y = size // 2, size // 2
    num = 1
    board[x][y] = num
    y += 1
    num += 1
    movement = UP
    while in_bounds(x, y, size):
        if neighbor(movement, x, y, board) is not None:
            board[x][y] = num
            x, y = update(movement, x, y)
            num += 1
        else:
            movement = next_movement[movement]

# Adapted from "Pi Delport" on stackoverflow
def primes_sieve(limit):
    a = [True] * limit
    a[0] = a[1] = False
    ans = set()
    for (i, isprime) in enumerate(a):
        if isprime:
            ans.add(i)
            for n in range(i*i, limit, i):
                a[n] = False 
    return ans

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-size", type=int, default=201)
parser.add_argument("-bg", type=str, default="blue")
parser.add_argument("-color", type=str, default="red")
parser.add_argument("-radius", type=int, default=1)

args = parser.parse_args()

if args.size % 2 != 1:
    raise Exception("please ensure size is odd.")

multiplier = 2 * args.radius

primes = primes_sieve(args.size ** 2)

board = [[None for i in range(args.size)] for j in range(args.size)]
spiralize(board)

win = GraphWin("Prime Ulam Spiral (size {}) ".format(args.size),
                args.size * multiplier,
                args.size * multiplier,
                autoflush=False)
win.setBackground(args.bg)

for i in range(len(board)):
    for j in range(len(board)):
        if board[i][j] in primes:
            c = Circle(Point(i* multiplier, j * multiplier), args.radius)
            c.setFill(args.color)
            c.setOutline(args.color)
            c.draw(win)

# To force instant drawing
for i in range(1):
    update(0,0,1)

win.getMouse()
win.close()
