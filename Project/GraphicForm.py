import os
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from os.path import sep
import sys
from Consts import len_board, len_side, pos_x, pos_y, EMPTY, NONE_COLOR, BLACK, WHITE
from ChessEngine import ChessEngine

# создание главного меню
class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = ChessEngine()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Шахматы")
        self.setFixedSize(900, 900)
        self.main()
        self.show()
        
    def main(self):
        # название для главного окна
        main_widget = QtWidgets.QWidget(self)
        self.labelGameName = QtWidgets.QLabel(main_widget)
        self.labelGameName.setGeometry(QtCore.QRect(385, 100, 455, 60))
        self.labelGameName.setStyleSheet("font: 18pt \"Arial\";")
        self.labelGameName.setObjectName("labelGameName")
        self.labelGameName.setText('Шахматы')
        # кнопка начала игры
        self.BtnPlay = QtWidgets.QPushButton(main_widget)
        self.BtnPlay.setGeometry(QtCore.QRect(120, 180, 660, 120))
        self.BtnPlay.setStyleSheet("font: 18pt \"Arial\";")
        self.BtnPlay.setObjectName("BtnPlay")
        self.BtnPlay.setText('Играть')
        self.BtnPlay.clicked.connect(self.game)
        # кнопка окна правил
        self.BtnRules = QtWidgets.QPushButton(main_widget)
        self.BtnRules.setGeometry(QtCore.QRect(120, 320, 660, 120))
        self.BtnRules.setStyleSheet("font: 18pt \"Arial\";")
        self.BtnRules.setObjectName("BtnRules")
        self.BtnRules.setText('Правила')
        self.BtnRules.clicked.connect(self.rules)
        # кнопка выхода
        self.BtnClose = QtWidgets.QPushButton(main_widget)
        self.BtnClose.setGeometry(QtCore.QRect(120, 460, 660, 120))
        self.BtnClose.setStyleSheet("font: 18pt \"Arial\";")
        self.BtnClose.setObjectName("BtnClose")
        self.BtnClose.setText('Выход')
        self.BtnClose.clicked.connect(sys.exit)
        self.setCentralWidget(main_widget)
    
    def rules(self):
        # виджет для отображения правил
        rules_widget = QtWidgets.QWidget(self)
        self.web = QWebEngineView(rules_widget)
        self.web.resize(900, 900)
        self.web.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.web.load(QUrl("file:///files//rules.pdf"))
        # кнопка для выхода из окна с правилами
        self.BtnCloseRules = QtWidgets.QPushButton(rules_widget)
        self.BtnCloseRules.setGeometry(QtCore.QRect(QtCore.QPoint(810, 5),QtCore.QPoint(870, 40)))
        self.BtnCloseRules.clicked.connect(self.main)
        self.BtnCloseRules.setText('Назад')
        self.setCentralWidget(rules_widget)
        
    def game(self):
        # отображение шахматной доски
        game_widget = QtWidgets.QWidget(self)
        self.desc_label = QtWidgets.QLabel(game_widget)
        self.desc_label.setGeometry(QtCore.QRect(QtCore.QPoint(pos_x, pos_y),
                                                 QtCore.QPoint(pos_x + len_board, pos_y + len_board)))
        self.desc_label.setPixmap(QtGui.QPixmap(f'files{sep}board.png'))
        # кнопка для смены стороны
        self.rotate_button = QtWidgets.QPushButton(game_widget)
        self.rotate_button.setGeometry(QtCore.QRect(QtCore.QPoint(590, 10), QtCore.QPoint(715, 50)))
        self.rotate_button.setStyleSheet("font: 9pt \"Arial\";")
        self.rotate_button.setObjectName("rotate_button")
        self.rotate_button.setText('Сменить сторону')
        self.rotate_button.clicked.connect(self.rotate)
        # кнопка для выхода в меню
        self.BtnBackToMenu = QtWidgets.QPushButton(game_widget)
        self.BtnBackToMenu.setGeometry(QtCore.QRect(QtCore.QPoint(720, 10), QtCore.QPoint(830, 50)))
        self.BtnBackToMenu.setStyleSheet("font: 9pt \"Arial\";")
        self.BtnBackToMenu.setObjectName("BtnBackToMenu")
        self.BtnBackToMenu.setText('Назад в меню')
        self.BtnBackToMenu.clicked.connect(self.main)
        # кнопка для ресета
        self.reset_button = QtWidgets.QPushButton(game_widget)
        self.reset_button.setGeometry(QtCore.QRect(QtCore.QPoint(460, 10), QtCore.QPoint(585, 50)))
        self.reset_button.setStyleSheet("font: 9pt \"Arial\";")
        self.reset_button.setObjectName("BtnBackToMenu")
        self.reset_button.setText('Заново')
        self.reset_button.clicked.connect(self.engine.__init__)
        self.reset_button.clicked.connect(self.update_board)
        # создание сетки кнопок и инициализация каждой кнопки с помощью данных из шахматного движка
        self.board = [[QtWidgets.QPushButton(game_widget) for j in range(8)] for i in range(8)]
        [[piece_init(k, m) for k, m in zip(i, j)] for i, j in zip(self.board, self.engine.board)]
        # кнопки для выбора фигур после превращения пешки
        self.widget_transformation = QtWidgets.QWidget(game_widget)
        self.widget_transformation.setGeometry(QtCore.QRect(
            QtCore.QPoint(pos_x + len_board // 2 - len_side * 2 - 20, pos_y + len_board // 2 - len_side // 2 - 20),
            QtCore.QPoint(pos_x + len_board // 2 + len_side * 2 + 20, pos_y + len_board // 2 + len_side // 2 + 20)))
        self.widget_transformation.setStyleSheet('background-color: gray')
        self.widget_transformation.setVisible(False)
        self.pack = [QtWidgets.QPushButton(self.widget_transformation) for i in range(4)]
        # окно завершения игры
        self.widget_game_over = QtWidgets.QWidget(game_widget)
        self.widget_game_over.setGeometry(QtCore.QRect(
            QtCore.QPoint(pos_x + len_board // 2 - len_side * 2 - 60, pos_y + len_board // 2 - len_side // 2 - 60),
            QtCore.QPoint(pos_x + len_board // 2 + len_side * 2 + 60, pos_y + len_board // 2 + len_side // 2 + 60)))
        self.widget_game_over.setStyleSheet('background-color: gray')
        self.game_over_text = QtWidgets.QLabel(self.widget_game_over)
        self.game_over_text.setGeometry(
            QtCore.QRect(
                QtCore.QPoint(self.widget_game_over.width() // 2 - 60, self.widget_game_over.height() // 2 - 50),
                QtCore.QPoint(self.widget_game_over.width() // 2 + 60, self.widget_game_over.height() // 2 - 20)))
        self.game_over_text.setAlignment(QtCore.Qt.AlignHCenter)
        # кнопка новой игры
        self.restart_button = QtWidgets.QPushButton(self.widget_game_over)
        self.restart_button.setGeometry(
            QtCore.QRect(
                QtCore.QPoint(self.widget_game_over.width() // 2 - 45, self.widget_game_over.height() // 2 - 30),
                QtCore.QPoint(self.widget_game_over.width() // 2 + 45, self.widget_game_over.height() // 2 + 30)))
        self.restart_button.setStyleSheet('background-color: white')
        self.restart_button.setText('Играть снова')
        self.restart_button.clicked.connect(self.restart)
        self.widget_game_over.setVisible(False)
        self.update_board()
        self.setCentralWidget(game_widget)
    # функция обновления доски
    def update_board(self):
        [[piece_update(k, m) for k, m in zip(i, j)] for i, j in zip(self.board, self.engine.board)]
        try:
            [[k.clicked.disconnect() for k in i] for i in self.board]
        except TypeError:
            pass
        [[k.clicked.connect(lambda f=False, m=m: self.send_request(m))
          for k, m in zip(i, j)] for i, j in zip(self.board, self.engine.board)]
    # функция поворота доски и обновления состояния доски
    def rotate(self):
        self.engine.rotate()
        self.update_board()

    def send_request(self, piece):
        self.engine.request_select(piece.pos)
        self.update_board()
        [[k.setIcon(QtGui.QIcon()) for k, m in zip(i, j) if m.name == EMPTY]
         for i, j in zip(self.board, self.engine.board)]
        [self.board[i[0]][i[1]].setIcon(QtGui.QIcon(f'files{os.path.sep}move.png'))
         for i in self.engine.active_spots['step']]
        [self.board[i[0]][i[1]].setIcon(QtGui.QIcon(f'files{os.path.sep}attack.png'))
         for i in self.engine.active_spots['takes']]
        if self.engine.last_touched != ():
            pos = self.engine.last_touched
            self.transform_request(pos)
            self.engine.last_touched = ()
        if self.engine.game_over:
            self.game_over()
    # функция включения кнопок после превращения пешки
    def transform_func(self):
        self.BtnBackToMenu.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.rotate_button.setEnabled(True)
        self.widget_transformation.setVisible(False)
        self.update_board()
        if self.engine.game_over:
            self.game_over()

    def transform_request(self, pos):
        self.BtnBackToMenu.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.rotate_button.setEnabled(False)
        self.widget_transformation.setVisible(True)
        for i, j in zip(self.pack, self.engine.transformation_pack()):
            piece_init(i, j, 20, 20)
            try:
                i.clicked.disconnect()
            except TypeError:
                pass
            i.clicked.connect(lambda f=False, j=j, pos=pos: self.engine.transform_request(j,
                                                                                          pos,
                                                                                          self.transform_func))
        self.engine.color = NONE_COLOR
    # функция окончания игры
    def game_over(self):
        if self.engine.draw:
            self.engine.color = NONE_COLOR
            self.game_over_text.setText('Ничья')
        else:
            if self.engine.stalemate:
                self.game_over_text.setText('Пат')
            else:
                if self.engine.color == BLACK:
                    self.game_over_text.setText('Победили белые')
                else:
                    self.game_over_text.setText('Победили чёрные')
        self.BtnBackToMenu.setEnabled(False)
        self.rotate_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.widget_game_over.setVisible(True)
    # функция для игры снова
    def restart(self):
        self.widget_game_over.setVisible(False)
        self.engine.__init__()
        self.update_board()
        self.BtnBackToMenu.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.rotate_button.setEnabled(True)

# функция установки положения и размера фигур
def piece_init(board_piece, engine_piece, x=pos_x, y=pos_y):
    piece_update(board_piece, engine_piece)
    board_piece.setIconSize(QtCore.QSize(70, 70))
    board_piece.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: none;")
    board_piece.setGeometry(QtCore.QRect(
        QtCore.QPoint(x + engine_piece.pos[1] * len_side,
                      y + engine_piece.pos[0] * len_side),
        QtCore.QPoint(x + engine_piece.pos[1] * len_side + len_side,
                      y + engine_piece.pos[0] * len_side + len_side)))

# функция обновления визуального представления шахматной фигуры на доске
def piece_update(board_piece, engine_piece):
    board_piece.setIcon(QtGui.QIcon(engine_piece.image))
