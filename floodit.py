# ------------------------------
# Imports
# ------------------------------

from guizero import App, Waffle, Text, PushButton, info
import random

# ------------------------------
# Variables
# ------------------------------

colours = ["red", "blue", "green", "yellow", "magenta", "purple"]
board_size = 14
moves_limit = 25
moves_taken = 0
moves_countdown = moves_limit

# ------------------------------
# Functions
# ------------------------------

# Recursively floods adjacent squares
def flood(x, y, target, replacement):
    # Algorithm from https://en.wikipedia.org/wiki/Flood_fill
    if target == replacement:
        return False
    if board.get_pixel(x, y) != target:
        return False
    board.set_pixel(x, y, replacement)
    if y+1 <= board_size-1:   # South
        flood(x, y+1, target, replacement)
    if y-1 >= 0:            # North
        flood(x, y-1, target, replacement)
    if x+1 <= board_size-1:    # East
        flood(x+1, y, target, replacement)
    if x-1 >= 0:            # West
        flood(x-1, y, target, replacement)

# Check whether all squares are the same
def all_squares_are_the_same():
    squares = board.get_all()
    if all(colour == squares[0] for colour in squares):
        return True
    else:
        return False

def win_check():
    global moves_taken
    moves_taken += 1
    moves_countdown = str(moves_limit - moves_taken)
    win_text.value = "Moves: " + str(moves_countdown)
    if moves_taken < moves_limit:
        if all_squares_are_the_same():
            win_text.value = "You win!\nClick on any color to start a new game."
    else:
        win_text.value = "You lost :(\nClick on any color to start a new game."
    if moves_taken > moves_limit:
        moves_taken = 0
        fill_board()
    
def fill_board():
    moves_countdown = str(moves_limit - moves_taken)
    win_text.value = "Moves: " + str(moves_countdown)
    for x in range(board_size):
        for y in range(board_size):
            board.set_pixel(x, y, random.choice(colours))

def init_palette():
    for colour in colours:
        palette.set_pixel(colours.index(colour), 0, colour)

def start_flood(x, y):
    flood_colour = palette.get_pixel(x,y)
    target = board.get_pixel(0,0)
    flood(0, 0, target, flood_colour)
    win_check()


# ------------------------------
# App
# ------------------------------

app = App("Flood it")

board = Waffle(app, width=board_size, height=board_size, pad=0)
palette = Waffle(app, width=6, height=1, dotty=True, command=start_flood)

win_text = Text(app)

fill_board()
init_palette()

app.display()
