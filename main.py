import tkinter as tk
from PIL import Image, ImageTk
import os
# import game_classes

# Change to data dir
cwd = os.getcwd()
print(cwd)
os.chdir('data')

# Create canvas
root = tk.Tk()
root.resizable(False, False)
root.title('Chess')

canvas = tk.Canvas(root, width=640, height=640, bd=0, highlightthickness=0)
canvas.grid(columnspan=8, rowspan=8)
canvas.configure(background='black')
# ------------------------- Variables ------------------------- #


# Images
b_queen = Image.open('b_queen.png')
b_queen = ImageTk.PhotoImage(b_queen)

w_queen = Image.open('w_queen.png')
w_queen = ImageTk.PhotoImage(w_queen)

b_bishop = Image.open('b_bishop.png')
b_bishop = ImageTk.PhotoImage(b_bishop)

w_bishop = Image.open('w_bishop.png')
w_bishop = ImageTk.PhotoImage(w_bishop)

b_rook = Image.open('b_rook.png')
b_rook = ImageTk.PhotoImage(b_rook)

w_rook = Image.open('w_rook.png')
w_rook = ImageTk.PhotoImage(w_rook)

w_pawn = Image.open('w_pawn.png')
w_pawn = ImageTk.PhotoImage(w_pawn)

b_pawn = Image.open('b_pawn.png')
b_pawn = ImageTk.PhotoImage(b_pawn)

w_knight = Image.open('w_knight.png')
w_knight = ImageTk.PhotoImage(w_knight)

b_knight = Image.open('b_knight.png')
b_knight = ImageTk.PhotoImage(b_knight)

w_king = Image.open('w_king.png')
w_king = ImageTk.PhotoImage(w_king)

b_king = Image.open('b_king.png')
b_king = ImageTk.PhotoImage(b_king)

blank = Image.open('blank.png')
blank = ImageTk.PhotoImage(blank)

# Game variables
convert_x_to_letter = {0: 'a', 1: 'b', 2: 'c',
                       3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

tiles = []

chess_piece_locs = {
    'a1': w_rook, 'b1': w_knight, 'c1': w_bishop, 'd1': w_queen, 'e1': w_king, 'f1': w_bishop, 'g1': w_knight, 'h1': w_rook,
    'a8': b_rook, 'b8': b_knight, 'c8': b_bishop, 'e8': b_queen, 'd8': b_king, 'f8': b_bishop, 'g8': b_knight, 'h8': b_rook,
    'a2': w_pawn, 'b2': w_pawn, 'c2': w_pawn, 'd2': w_pawn, 'e2': w_pawn, 'f2': w_pawn, 'g2': w_pawn, 'h2': w_pawn,
    'a7': b_pawn, 'b7': b_pawn, 'c7': b_pawn, 'd7': b_pawn, 'e7': b_pawn, 'f7': b_pawn, 'g7': b_pawn, 'h7': b_pawn}

black_pieces = [b_rook, b_king, b_bishop, b_knight, b_pawn, b_queen]
white_pieces = [w_rook, w_king, w_bishop, w_knight, w_pawn, w_queen]

# ----------------------------- Making the board ----------------------------- #

# Tiles


def conv_pos(pos):
    y = 8 - pos[1]
    x = convert_x_to_letter[pos[0]]
    return (f'{x}{y}')


class Tiles:
    def __init__(self, pos, occupied_by, color):
        # self.pos = pos(pos)
        self.pos = pos
        self.occupied_by = occupied_by
        self.color = color
        self.func = tk.Button(root, borderwidth=0,
                              command=lambda: select_piece(self.pos))
        self.func.config(height=80, width=80, compound='left',
                         bg=self.color, activebackground="#48bf53")
        self.func.grid(column=pos[0], row=pos[1])


for x in range(8):
    for y in range(8):
        if (x % 2 != 0 and y % 2 == 0) or (y % 2 != 0 and x % 2 == 0):
            color = '#b48b64'
        else:
            color = '#f4dbb4'

        tile = Tiles([x, y], False, color=color)
        tiles.append(tile)
        for loc in chess_piece_locs:
            if conv_pos([x, y]) in chess_piece_locs:
                tile.func.config(
                    image=chess_piece_locs[conv_pos([x, y])], height=80, width=80)
                tile.occupied_by = chess_piece_locs[conv_pos([x, y])]
            else:
                tile.func.config(image=blank, height=80, width=80)
                tile.occupied_by = None


# ----------------------------- Game functions ----------------------------- #


# Move piece functions


class Selection:  # Create class to store global variables
    def __init__(self):
        self.select_time = 0
        self.cur_pos = None
        self.des_pos = None
        self.path = None
        self.turns = 1  # if turns is indivisible by 2 than it's white's turn
        self.cur_tile = None
        self.des_tile = None
        self.b_king_move = False
        self.w_king_move = False


selection = Selection()


def select_piece(pos):
    print(pos)
    selection.select_time += 1
    if selection.select_time == 1:
        selection.cur_pos = pos
        for tile in tiles:
            if tile.pos == pos:
                occupied = tile.occupied_by
        if occupied == None:  # Prevent player from moving blank pieces
            selection.select_time = 0
    elif selection.select_time == 2:
        selection.des_pos = pos
        if selection.cur_pos == selection.des_pos:  # Prevent self destruction
            print(f'Move is not valid!')
            selection.select_time = 0
        elif not_friendly_fire() == False:
            selection.select_time = 0

        else:
            selection.select_time = 0
            move_pieces()


def not_friendly_fire():
    cur_side = selection.cur_tile.occupied_by
    des_side = selection.des_tile.occupied_by

    if des_side == None:
        return True

    if cur_side in black_pieces and des_side in black_pieces:
        return False

    elif cur_side in white_pieces and des_side in white_pieces:
        return False

    else:
        return True


def move_turn():
    if selection.turns % 2 == 0:
        turn = 'white'
    else:
        turn = 'black'

    if turn == 'white':
        if selection.cur_tile.occupied_by in black_pieces:
            return False
        else:
            True

    else:
        if selection.cur_tile.occupied_by in white_pieces:
            return False

        else:
            True


def move_pieces():
    for tile in tiles:
        if tile.pos == selection.cur_pos:
            selection.cur_tile = tile
        if tile.pos == selection.des_pos:
            selection.des_tile = tile

    if is_valid(selection.cur_pos, selection.des_pos, selection.cur_tile.occupied_by) and not_friendly_fire() and move_turn() == False:
        # Delete image in the current tile
        selection.cur_tile.func.config(image=blank)
        # Move image in the destinated tile
        selection.des_tile.func.config(image=selection.cur_tile.occupied_by)
        selection.des_tile.occupied_by = selection.cur_tile.occupied_by
        selection.cur_tile.occupied_by = None
        print(
            f'Turn {selection.turns}: {conv_pos(selection.cur_pos)} to {conv_pos(selection.des_pos)}.')
        selection.turns += 1
    else:
        print(f'Move is not valid!')


# Check if move is valid

def find_piece(pos):
    for tile in tile:
        if tile.pos == pos:
            return tile.occupied_by


def is_valid(cur_pos, des_pos, occupied_by):
    if occupied_by == b_rook or occupied_by == w_rook:  # Allow moving horizontally
        if cur_pos[0] == des_pos[0] or cur_pos[1] == des_pos[1]:
            return True

    if occupied_by == b_bishop or occupied_by == w_bishop:  # Allow moving diagonally
        if abs(cur_pos[0] - des_pos[0]) == abs(cur_pos[1] - des_pos[1]):
            return True

    if occupied_by == b_queen or occupied_by == w_queen:  # Allow moving diagonally and horizontally
        if cur_pos[0] == des_pos[0] or cur_pos[1] == des_pos[1]:
            return True
        if abs(cur_pos[0] - des_pos[0]) == abs(cur_pos[1] - des_pos[1]):
            return True

    if occupied_by == b_king or occupied_by == w_king:
        # Allow moving 1 tile every side
        if abs(cur_pos[0] - des_pos[0]) < 2 and abs(cur_pos[1] - des_pos[1]) < 2:
            return True

        # Allow castling
        if find_piece([5, 7]) == blank and find_piece([6, 7]) == blank:
            pass

    if occupied_by == w_pawn:
        if cur_pos[1] == 6:  # Allow moving up 2 tiles at the start
            if (cur_pos[0] == des_pos[0]) and (cur_pos[1] - des_pos[1] == 2):
                return True
        # Moving up 1 tile at a time
        if (cur_pos[0] == des_pos[0]) and (cur_pos[1] - des_pos[1] == 1):
            return True

        # Allow capturing diagonally
        if abs(cur_pos[0] - des_pos[0]) == 1 and (cur_pos[1] - des_pos[1]) == 1:
            return True

    if occupied_by == b_pawn:
        if cur_pos[1] == 1:  # Allow going up 2 tiles at the start
            if (cur_pos[0] == des_pos[0]) and (cur_pos[1] - des_pos[1] == -2):
                return True

        # Moving up 1 tile at a time
        if (cur_pos[0] == des_pos[0]) and (cur_pos[1] - des_pos[1] == -1):
            return True

        # Allow capturing diagonally
        if abs(cur_pos[0] - des_pos[0]) == 1 and (des_pos[1] - cur_pos[1]) == 1:
            return True

    if occupied_by == b_knight or occupied_by == w_knight:
        # Moving in a wide L shape
        if abs(cur_pos[0] - des_pos[0]) == 1 and abs(cur_pos[1] - des_pos[1]) == 2:
            return True
        # Moving in a high L shape
        if abs(cur_pos[0] - des_pos[0]) == 2 and abs(cur_pos[1] - des_pos[1]) == 1:
            return True


def castle():
    if selection.b_king_move == False:
        for tile in tiles:
            if tile.pos == [3, 0]:
                b_king_tile = tile
        if b_king_tile.occupied_by != b_king:
            selection.b_king_move = True

    if selection.w_king_move == False:
        for tile in tiles:
            if tile.pos == [4, 7]:
                w_king_tile = tile
        if w_king_tile.occupied_by != w_king:
            selection.w_king_move = True


def clear_path(cur_pos, des_pos, occupied_by):
    # For vertical movement
    if occupied_by == w_rook or occupied_by == b_rook or occupied_by == w_queen or occupied_by == b_queen:
        for i in range(cur_pos[0], des_pos[0]):
            pass


root.mainloop()

# print('tôi chầm cãm wá')
