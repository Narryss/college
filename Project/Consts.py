import os
from PIL import Image

BLACK = 'black'
WHITE = 'white'
NONE_COLOR = 'Zcolor'
EMPTY = 'empty'
PAWN = 'pawn'
KNIGHT = 'knight'
KING = 'king'
BISHOP = 'bishop'
ROCK = 'rock'
QUEEN = 'queen'
NONE_SPOTS = {'step': [], 'takes': []}
NONE_SELECT = {'pos1': (), 'pos2': ()}
len_board = Image.open(f'files{os.path.sep}board.png').size[0]
pos_x, pos_y, len_side = 66, 66, len_board // 8
# допустимые перемещения для фигур
UPPER = {
    PAWN: {
        'step': ((1, 0),),
        'takes': ((1, -1), (1, 1)),
    },

    KNIGHT: {
        'step': ((1, 2), (-1, 2), (-1, -2), (1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)),
    },

    BISHOP: {
        'step': ((1, 1), (-1, 1), (-1, -1), (1, -1))
    },

    ROCK: {
        'step': ((1, 0), (-1, 0), (0, 1), (0, -1))
    },

    QUEEN: {
        'step': ((1, 1), (-1, 1), (-1, -1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
    },

    KING: {
        'step': ((1, 1), (-1, 1), (-1, -1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)),
    }
}

DOWN = {
    PAWN: {
        'step': ((-1, 0),),
        'takes': ((-1, -1), (-1, 1)),
    },
    KNIGHT: UPPER[KNIGHT],
    BISHOP: UPPER[BISHOP],
    ROCK: UPPER[ROCK],
    QUEEN: UPPER[QUEEN],
    KING: UPPER[KING]
}
# расположение фигур на доске
board_preset = [
    (
        (ROCK, (0, 0), BLACK),
        (KNIGHT, (0, 1), BLACK),
        (BISHOP, (0, 2), BLACK),
        (QUEEN, (0, 3), BLACK),
        (KING, (0, 4), BLACK),
        (BISHOP, (0, 5), BLACK),
        (KNIGHT, (0, 6), BLACK),
        (ROCK, (0, 7), BLACK),
    ),
    (
        (PAWN, (1, 0), BLACK),
        (PAWN, (1, 1), BLACK),
        (PAWN, (1, 2), BLACK),
        (PAWN, (1, 3), BLACK),
        (PAWN, (1, 4), BLACK),
        (PAWN, (1, 5), BLACK),
        (PAWN, (1, 6), BLACK),
        (PAWN, (1, 7), BLACK),
    ),
    *tuple(tuple((EMPTY, (i, j)) for j in range(8)) for i in range(2, 6)),
    (
        (PAWN, (6, 0), WHITE, DOWN),
        (PAWN, (6, 1), WHITE, DOWN),
        (PAWN, (6, 2), WHITE, DOWN),
        (PAWN, (6, 3), WHITE, DOWN),
        (PAWN, (6, 4), WHITE, DOWN),
        (PAWN, (6, 5), WHITE, DOWN),
        (PAWN, (6, 6), WHITE, DOWN),
        (PAWN, (6, 7), WHITE, DOWN),
    ),
    (
        (ROCK, (7, 0), WHITE, DOWN),
        (KNIGHT, (7, 1), WHITE, DOWN),
        (BISHOP, (7, 2), WHITE, DOWN),
        (QUEEN, (7, 3), WHITE, DOWN),
        (KING, (7, 4), WHITE, DOWN),
        (BISHOP, (7, 5), WHITE, DOWN),
        (KNIGHT, (7, 6), WHITE, DOWN),
        (ROCK, (7, 7), WHITE, DOWN),
    ),
]
