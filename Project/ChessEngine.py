import Pieces as Pc
from Consts import *


class ChessEngine:
    def __init__(self):
        self.color = WHITE
        self.board = []
        self.kings = []
        self.active_spots = NONE_SPOTS
        self.select = NONE_SELECT
        self.last_touched = ()
        self.draw = False
        self.stalemate = False
        self.game_over = False
        self.clear_memory()
        self.init_board()
    # инициализация шахматной доски
    def init_board(self):
        for i in range(8):
            self.board.append([])
            for j in range(8):
                self.board[i].append(Pc.EMPTY)
        for preset in Pc.board_preset:
            for piece in preset:
                self.board[piece[1][0]][piece[1][1]] = Pc.Piece(*piece)
        self.kings = [self.board[0][4], self.board[7][4]]
    # функция смены стороны
    def rotate(self):
        self.board = list(zip(*tuple(zip(*self.board[::-1]))[::-1]))
        self.board = [list(i) for i in self.board]
        for i in self.board:
            for piece in i:
                if piece.name == PAWN:
                    if piece.step == ((1, 0),):
                        piece.step = ((-1, 0),)
                        piece.takes = ((-1, -1), (-1, 1))
                    else:
                        piece.step = ((1, 0),)
                        piece.takes = ((1, -1), (1, 1))
                piece.pos = (self.board.index(i), i.index(piece))
    # получает от пользователя фигуру и обрабатывает её
    def request_select(self, pos: list):
        if self.color == NONE_COLOR:
            return
        piece = self.board[pos[0]][pos[1]]
        if self.is_selected:
            self.update_spot(pos2=piece.pos)
            if piece.pos in self.active_spots['step']:
                self.request_move()
            elif piece.pos in self.active_spots['takes']:
                self.request_take()
            else:
                self.clear_memory()
                return
            self.clear_memory()
            self.color = WHITE if self.color == BLACK else BLACK
            self.is_game_over()
            return
        if piece.name == EMPTY or piece.color != self.color:
            self.clear_memory()
            return
        available_steps, available_takes = self.get_available_moves(pos)
        if [available_steps, available_takes] == [(), ()]:
            self.clear_memory()
            return
        self.is_selected = True
        self.update_spot(pos1=piece.pos)
        self.active_spots.update({'step': available_steps, 'takes': available_takes})
        if self.active_spots == {'step': [], 'takes': []}:
            self.clear_memory()
    # обеспечивает чтобы возможные ходы и захваты не ставили короля под шах
    def get_available_moves(self, pos):
        piece = self.board[pos[0]][pos[1]]
        if piece.name == EMPTY:
            return [(), ()]
        available_steps, available_takes = self.calc_possible_moves(pos)
        for moves in [available_takes, available_steps]:
            remove = []
            for i in moves:
                board = []
                for j in self.board:
                    board.append([])
                    for k in j:
                        board[self.board.index(j)].append(k)
                board[pos[0]][pos[1]], board[i[0]][i[1]] = Pc.Piece(EMPTY, (pos[0], pos[1])), board[pos[0]][pos[1]]
                answer = self.king_under_attack(board)
                if answer is not None:
                    for king in answer:
                        if king.color == piece.color:
                            remove.append(i)
            for i in remove:
                try:
                    moves.remove(i)
                except ValueError:
                    continue
        if [available_steps, available_takes] == [[], []]:
            return [(), ()]
        return [available_steps, available_takes]
    # проверяет доступность ходов
    def calc_possible_moves(self, pos, board=None):
        if board is None:
            board = self.board.copy()
        piece = board[pos[0]][pos[1]]
        if piece.name == EMPTY:
            return [(), ()]
        available_steps, available_takes = [], []
        if not piece.linear:
            for i in piece.step:
                step = (pos[0] + i[0], pos[1] + i[1])
                if all(0 <= s <= 7 for s in step):
                    if board[step[0]][step[1]].name == EMPTY:
                        available_steps.append(step)
            for i in piece.takes:
                take = (pos[0] + i[0], pos[1] + i[1])
                if all(0 <= s <= 7 for s in take):
                    if (board[take[0]][take[1]].name != EMPTY and
                            board[take[0]][take[1]].color != piece.color):
                        available_takes.append(take)
        else:
            for i in piece.step:
                checking_pos = piece.pos
                while True:
                    checking_pos = (checking_pos[0] + i[0], checking_pos[1] + i[1])
                    if not all(0 <= s <= 7 for s in checking_pos):
                        break
                    if board[checking_pos[0]][checking_pos[1]].name == EMPTY:
                        available_steps.append(checking_pos)
                    else:
                        break
            for i in piece.step:
                checking_pos = piece.pos
                while True:
                    checking_pos = (checking_pos[0] + i[0], checking_pos[1] + i[1])
                    if not all(0 <= s <= 7 for s in checking_pos):
                        break
                    if (board[checking_pos[0]][checking_pos[1]].name != EMPTY and
                            board[checking_pos[0]][checking_pos[1]].color != piece.color):
                        available_takes.append(checking_pos)
                        break
                    elif (board[checking_pos[0]][checking_pos[1]].name != EMPTY and
                          board[checking_pos[0]][checking_pos[1]].color == piece.color):
                        break
        exceptions = self.base_exceptions_select(piece, board)
        if exceptions is not None:
            if exceptions['step'] != ():
                [available_steps.append(i) for i in exceptions['step']]
            if exceptions['takes'] != ():
                [available_takes.append(i) for i in exceptions['takes']]
        return [available_steps, available_takes]
    # обновление позиций в словаре
    def update_spot(self, pos1=None, pos2=None):
        if pos1 is not None:
            self.select.update({'pos1': pos1})
        elif pos2 is not None:
            self.select.update({'pos2': pos2})
        if self.select['pos1'] == self.select['pos2']:
            self.clear_memory()
    # очистка состояния объекта
    def clear_memory(self):
        self.active_spots.update({'step': [], 'takes': []})
        self.select.update({'pos1': (), 'pos2': ()})
        self.is_selected = False

    # выполнение специальных ходов для пешек и королей
    def request_move(self):
        x1, y1, x2, y2 = self.select['pos1'][0], self.select['pos1'][1], self.select['pos2'][0], self.select['pos2'][1]
        is_pass = self.base_exceptions_move(x1, y1, x2, y2)
        if is_pass:
            self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]
            self.board[x1][y1].pos, self.board[x2][y2].pos = (x1, y1), (x2, y2)
            self.board[x2][y2].is_moved = True
        for i in self.board:
            for j in i:
                if j.name == PAWN and j != self.board[x2][y2]:
                    j.is_exception_step_used = False
        self.clear_memory()
    # выполнение специальных ходов для пешек
    def request_take(self):
        x1, y1, x2, y2 = self.select['pos1'][0], self.select['pos1'][1], self.select['pos2'][0], self.select['pos2'][1]
        is_pass = self.base_exceptions_take(x1, y1, x2, y2)
        if is_pass:
            self.board[x1][y1], self.board[x2][y2] = Pc.Piece(EMPTY, (x1, y1)), self.board[x1][y1]
            self.board[x1][y1].pos, self.board[x2][y2].pos = (x1, y1), (x2, y2)
            self.board[x2][y2].is_moved = True
        for i in self.board:
            for j in i:
                if j.name == PAWN and j != self.board[x2][y2]:
                    j.is_exception_step_used = False
        self.clear_memory()
    # обработка специальных случаев для перемещения пешек и королей
    def base_exceptions_move(self, x1, y1, x2, y2):
        if self.board[x1][y1].name == PAWN:
            if abs(x1 - x2) == 2:
                self.board[x1][y1].is_exception_step_used = True
            elif self.board[x1][y1].step == ((1, 0),) and x2 == 7:
                self.last_touched = (x2, y2)
            elif self.board[x1][y1].step == ((-1, 0),) and x2 == 0:
                self.last_touched = (x2, y2)
            return True
        elif self.board[x1][y1].name == KING:
            if y1 - y2 in (2, 3) and x1 == x2:
                (self.board[x1][y1],
                 self.board[x2][y2],
                 self.board[x2][y2 + 1],
                 self.board[x1][0]) = (Pc.Piece(EMPTY, (x1, y1)),
                                       self.board[x1][y1],
                                       self.board[x2][0], Pc.Piece(EMPTY, (x1, 0)))
                self.board[x1][y1].pos, self.board[x2][y2].pos, self.board[x2][y2 + 1].pos = ((x1, y1),
                                                                                              (x2, y2),
                                                                                              (x2, y2 + 1))
                self.board[x1][y1].is_moved, self.board[x2][y2].is_moved = True, True
                return False
            elif y2 - y1 in (2, 3) and x1 == x2:
                (self.board[x1][y1],
                 self.board[x2][y2],
                 self.board[x2][y2 - 1],
                 self.board[x1][7]) = (Pc.Piece(EMPTY, (x1, y1)),
                                       self.board[x1][y1],
                                       self.board[x2][7], Pc.Piece(EMPTY, (x1, 7)))
                self.board[x1][y1].pos, self.board[x2][y2].pos, self.board[x2][y2 - 1].pos = ((x1, y1),
                                                                                              (x2, y2),
                                                                                              (x2, y2 - 1))
                self.board[x1][y1].is_moved, self.board[x2][y2].is_moved = True, True
                return False
        return True
    # взятие на проходе
    def base_exceptions_take(self, x1, y1, x2, y2):
        if self.board[x1][y1].name == PAWN:
            if self.board[x2][y2].name == EMPTY:
                self.board[x1][y1], self.board[x1][y2], self.board[x2][y2] = (Pc.Piece(EMPTY, (x1, y1)),
                                                                              Pc.Piece(EMPTY, (x1, y2)),
                                                                              self.board[x1][y1])
                self.board[x2][y2].pos, self.board[x2][y2].is_moved = (x2, y2), True
                return False
            elif self.board[x1][y1].step == ((1, 0),) and x2 == 7:
                self.last_touched = (x2, y2)
            elif self.board[x1][y1].step == ((-1, 0),) and x2 == 0:
                self.last_touched = (x2, y2)
            return True
        return True
    # проверяет возможные исключительные ходы для пешки и короля
    def base_exceptions_select(self, piece, board=None):
        if board is None:
            board = self.board.copy()
        exceptions = {'step': (), 'takes': ()}
        x, y = piece.pos
        if piece.name == PAWN:
            if not piece.is_moved:
                if (piece.step == ((1, 0),)
                        and board[x + 1][y].name == EMPTY
                        and board[x + 2][y].name == EMPTY):
                    exceptions.update({'step': ((x + 2, y),)})
                elif (piece.step == ((-1, 0),)
                      and board[x - 1][y].name == EMPTY
                      and board[x - 2][y].name == EMPTY):
                    exceptions.update({'step': ((x - 2, y),)})
            if 0 <= y - 1 <= 7:
                if board[x][y - 1].name == PAWN and board[x][y].color != board[x][y - 1].color:
                    if board[x][y - 1].is_exception_step_used:
                        if piece.step == ((1, 0),):
                            exceptions.update({'takes': ((x + 1, y - 1),)})
                        else:
                            exceptions.update({'takes': ((x - 1, y - 1),)})
            if 0 <= y + 1 <= 7:
                if board[x][y + 1].name == PAWN and board[x][y].color != board[x][y + 1].color:
                    if board[x][y + 1].is_exception_step_used:
                        if piece.step == ((1, 0),):
                            exceptions.update({'takes': ((x + 1, y + 1),)})
                        else:
                            exceptions.update({'takes': ((x - 1, y + 1),)})
        elif piece.name == KING:
            y1, y2, y1_legit, y2_legit = 0, 7, False, False
            if not piece.is_moved:
                if board[x][y1].name == ROCK:
                    if board[x][y1].color == piece.color and not board[x][y1].is_moved:
                        for i in range(y1 + 1, y):
                            if board[x][i].name == EMPTY:
                                y1_legit = True
                            else:
                                y1_legit = False
                                break
                if board[x][y2].name == ROCK:
                    if board[x][y2].color == piece.color and not board[x][y2].is_moved:
                        for i in range(y + 1, y2):
                            if board[x][i].name == EMPTY:
                                y2_legit = True
                            else:
                                y2_legit = False
                                break
                appends = []
                if y1_legit:
                    if abs(y1 - y) == 4:
                        appends.append((x, y - 2))
                    else:
                        appends.append((x, y + 2))
                if y2_legit:
                    if abs(y2 - y) == 4:
                        appends.append((x, y - 2))
                    else:
                        appends.append((x, y + 2))
                exceptions.update({'step': tuple(appends)})
        if exceptions != {'step': (), 'takes': ()}:
            return exceptions
        else:
            return None
    # пак для превращения пешки
    def transformation_pack(self):
        color = WHITE if self.color == BLACK else BLACK
        pack = ((QUEEN, (0, 0), color),
                (BISHOP, (0, 1), color),
                (KNIGHT, (0, 2), color),
                (ROCK, (0, 3), color))
        return [Pc.Piece(*i) for i in pack]
    # превращение пешки
    def transform_request(self, piece, pos, transform_func):
        x, y = pos
        self.color = WHITE if piece.color == BLACK else BLACK
        self.board[x][y] = Pc.Piece(piece.name, pos, piece.color)
        transform_func()
    # проверка находится ли король под атакой
    def king_under_attack(self, board):
        who_attacked = []
        king = [i for i in self.kings if i.color == self.color][0]
        for i in range(8):
            for j in range(8):
                if board[i][j].name != EMPTY:
                    steps, takes = self.calc_possible_moves((i, j), board)
                    king_pos = (0, 0)
                    for k in board:
                        for m in k:
                            if king == m:
                                king_pos = (board.index(k), k.index(m))
                                break
                    if king_pos in takes:
                        who_attacked.append(king)
                else:
                    continue
        if who_attacked is not None:
            return who_attacked
        else:
            return None
    # функция окончания игры
    def is_game_over(self):
        king = [i for i in self.kings if i.color == self.color][0]
        king_useless = True if self.get_available_moves(king.pos) == [(), ()] else False
        for i in self.board:
            flag = False
            for j in i:
                if j.color == self.color:
                    answer = self.get_available_moves(j.pos)
                    if answer != [(), ()]:
                        flag = True
                        break
            if flag:
                break
            elif self.board.index(i) == 7:
                self.game_over = True
                break
        if self.game_over:
            if king_useless and not self.king_under_attack(self.board):
                self.stalemate = True
                return
            else:
                return
        pieces = []
        for i in self.board:
            for j in i:
                if j.name != EMPTY:
                    pieces.append(j.name)
        if pieces != [KING, KING]:
            return
        else:
            self.draw = True
            self.game_over = True
            
