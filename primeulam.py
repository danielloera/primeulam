from graphics import *
import argparse

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

CIRCLE = "circle"
SQUARE = "square"
TRIANLGE = "triangle"

CIRCLE_NUM = 0
SQUARE_NUM = 1
TRIANLGE_NUM = 2

next_movement = {
            UP: LEFT,
            LEFT: DOWN,
            DOWN: RIGHT,
            RIGHT: UP
}

shape_convert = {
            CIRCLE: CIRCLE_NUM,
            SQUARE: SQUARE_NUM,
            TRIANLGE: TRIANLGE_NUM
}

def neighbor(curr_movement, x, y, board):
    if curr_movement == UP:
        return board[x][y - 1]
    if curr_movement == LEFT:
        return board[x + 1][y]
    if curr_movement == DOWN:
        return board[x][y + 1]
    return board[x - 1][y]

def move(curr_movement, x, y):
    if curr_movement == UP:
        return x - 1, y
    if curr_movement == LEFT:
        return x, y - 1
    if curr_movement == DOWN:
        return x + 1, y
    return x, y + 1

def spiralize(board, num):
    size = len(board)
    x, y = size // 2, size // 2
    board[x][y] = num
    movement = RIGHT
    x, y = move(movement, x, y)
    num += 1
    while x >= 0 and x < size and y >= 0 and y < size:
        if neighbor(movement, x, y, board) is not None:
            board[x][y] = num
            x, y = move(movement, x, y)
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

def get_shape(x, y, multiplier, shape, shape_size):
    x, y = x * multiplier, y * multiplier
    if shape == CIRCLE_NUM:
        return Circle(Point(x, y), shape_size)
    if shape == SQUARE_NUM:
        return Rectangle(
                Point(x - shape_size, y - shape_size),
                Point(x + shape_size, y + shape_size))
    return Polygon(
            Point(x, y),
            Point(x - multiplier, y + multiplier),
            Point(x + multiplier, y + multiplier))


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-size", type=int, default=201)
    parser.add_argument("-bg", type=str, default="blue")
    parser.add_argument("-color", type=str, default="red")
    parser.add_argument("-shape_size", type=float, default=1)
    parser.add_argument("-shape", type=str, default="circle")
    parser.add_argument("-start", type=int, default=1)

    args = parser.parse_args()

    if args.size % 2 != 1:
        raise Exception("please ensure size is odd.")

    # Scale board based on shape size
    multiplier = 2 * args.shape_size
    # Convert shape str into int for faster shape evaluation
    shape = shape_convert[args.shape]
    final_size = int(args.size * multiplier)

    primes = primes_sieve((args.size + args.start) ** 2)

    board = [[None for i in range(args.size)] for j in range(args.size)]
    spiralize(board, args.start)

    win = GraphWin("Prime Ulam Spiral (size {}) ".format(args.size),
                    final_size,
                    final_size,
                    autoflush=False)
    
    # Explicitly draw background so that it
    # Will properly save to file :)
    bg = Rectangle(
            Point(0, 0),
            Point(final_size, final_size))
    bg.setOutline(args.bg)
    bg.setFill(args.bg)
    bg.draw(win)

    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] in primes:
                s = get_shape(
                        x, y,
                        multiplier,
                        shape,
                        args.shape_size)
                s.setFill(args.color)
                s.setOutline(args.color)
                s.draw(win)

    win.getMouse()
    win.postscript(file="ulam.eps", colormode="color")
    from PIL import Image as NewImage
    img = NewImage.open("ulam.eps")
    img.save("ulam.png", "png")
    win.close()

    print("Raw image saved to ulam.eps")
    print("Actual size saved to ulam.png")

if __name__ == "__main__":
    main()
