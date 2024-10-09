from PyQt5 import QtGui
from Consts import *

# класс устанавления основных свойств фигурам
class Piece:
    def __init__(self, name: str, pos: tuple, color: str = WHITE, preset: dict = None):
        if preset is None:
            preset = UPPER
        self.name = name
        self.image = QtGui.QIcon('files{}{}{}{}.png'.format(os.path.sep, color, os.path.sep, name))
        self.pos = pos
        self.color = color
        self.is_moved = False
        if name != EMPTY:
            self.step = preset[name]['step']
        else:
            self.step = None
        if name in (ROCK, QUEEN, BISHOP):
            self.linear = True
        else:
            self.linear = False
        if name == PAWN:
            self.is_exception_step_used = False
            self.takes = preset[name]['takes']
        else:
            self.takes = self.step
