# coding: utf-8

import math
from collections import namedtuple
from pathlib import Path
from tkinter import Tk, Canvas, TRUE, BOTH

from PIL import ImageTk, Image

from ..core.data import Piece
from ..core.janggi import Janggi
from ..core.rule import next_coordinates


HORIZONTAL_LINES = 10
VERTICAL_LINES = 9
MARGIN_TOP = MARGIN_LEFT = 50
CELL_SIZE = 50
BOARD_WIDTH = CELL_SIZE * (VERTICAL_LINES - 1)
BOARD_HEIGHT = CELL_SIZE * (HORIZONTAL_LINES - 1)
BOARD_COLOR = '#F7931E'
CANVAS_WIDTH = BOARD_WIDTH + 2 * MARGIN_LEFT
CANVAS_HEIGHT = BOARD_HEIGHT + 2 * MARGIN_TOP

resource_dir = Path(__file__).resolve().parent / 'resource'
images = {
    Piece.Kung_a: 'Red_King',
    Piece.Kung_b: 'Green_King',
    Piece.Cha_a: 'Red_Cha',
    Piece.Cha_b: 'Green_Cha',
    Piece.Po_a: 'Red_Po',
    Piece.Po_b: 'Green_Po',
    Piece.Ma_a: 'Red_Ma',
    Piece.Ma_b: 'Green_Ma',
    Piece.Sang_a: 'Red_Sang',
    Piece.Sang_b: 'Green_Sang',
    Piece.Byung_a: 'Red_Byung',
    Piece.Jol_b: 'Green_Zol',
    Piece.Sa_a: 'Red_Sa',
    Piece.Sa_b: 'Green_Sa',
}

root = Tk()
root.geometry('{}x{}'.format(CANVAS_WIDTH, CANVAS_HEIGHT))
root.title(u'조선장기')
root.bind('<Escape>', lambda e: root.quit())

PieceInfo = namedtuple('PieceInfo', ('row', 'col', 'piece'))

class JanggiBoard:
    photoimages = {
        piece: ImageTk.PhotoImage(Image.open(
            resource_dir / (filename + '.png')
        ).resize((60, 54)))
        for piece, filename in images.items()
    }

    def __init__(self, *args, **kwargs):
        self.canvas = Canvas(
            width=CANVAS_HEIGHT, height=CANVAS_HEIGHT,
            background=BOARD_COLOR, *args, **kwargs
        )
        self.draw_hlines()
        self.draw_vlines()
        self.draw_palaces()
        self.canvas.bind('<Button-1>', self.on_button_pressed)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_released)
        self.canvas.bind('<Button1-Motion>', self.on_button_motion)
        self.board_state = Janggi(lambda x: self.update_canvas(self.board_state))
        self.board_state.reset()

    def draw_hlines(self):
        for i in range(HORIZONTAL_LINES):
            y = MARGIN_TOP + i * CELL_SIZE
            self.canvas.create_line(MARGIN_LEFT, y, MARGIN_LEFT + BOARD_WIDTH, y)

    def draw_vlines(self):
        for i in range(VERTICAL_LINES):
            x = MARGIN_LEFT + i * CELL_SIZE
            self.canvas.create_line(x, MARGIN_TOP, x, MARGIN_TOP + BOARD_HEIGHT)

    def draw_palaces(self):
        for i in (0, 7):
            y = MARGIN_TOP + i * CELL_SIZE
            self.canvas.create_line(
                MARGIN_LEFT + 3 * CELL_SIZE,
                y,
                MARGIN_TOP + 5 * CELL_SIZE,
                y + 2 * CELL_SIZE)
            self.canvas.create_line(
                MARGIN_LEFT + 5 * CELL_SIZE,
                y,
                MARGIN_TOP + 3 * CELL_SIZE,
                y + 2 * CELL_SIZE)

    def put_pieces(self, board):
        d = self.pieces = {}  # Map canvas item -> PieceInfo(row, col, piece)
        for i, row in enumerate(board):
            for j, piece in enumerate(row):
                if not piece:
                    continue
                item = self.canvas.create_image(
                    MARGIN_LEFT + j * CELL_SIZE,
                    MARGIN_TOP + i * CELL_SIZE,
                    image=self.photoimages[piece],
                    tags='piece')
                d[item] = PieceInfo(row=i, col=j, piece=piece)

    def update_canvas(self, board):
        self.canvas.delete('piece')
        self.put_pieces(self.board_state.board)

    def on_button_pressed(self, e):
        self.show_candidates(e)

    def on_button_released(self, e):
        if self.piece_to_move:
            self.move_piece(e)
        self.piece_to_move = None
        self.candidates = {}
        self.canvas.delete('candidate')

    def on_button_motion(self, e):
        if not self.piece_to_move:
            return
        self.canvas.move(self.piece_to_move, e.x - self.x, e.y - self.y)
        self.x, self.y = e.x, e.y

    def show_candidates(self, e):
        self.x, self.y = e.x, e.y
        self.piece_to_move = self.canvas.find_closest(e.x, e.y)
        self.candidates = {}
        try:
            r, c, p = self.pieces[self.piece_to_move[0]]
            if not self.board_state.can_move(p):
                raise KeyError
        except KeyError:
            self.piece_to_move = None
            return
        self.canvas.tag_raise(self.piece_to_move)
        for i, j in [(r, c)] + next_coordinates(self.board_state.board, r, c, p):
            item = self.canvas.create_oval(
                MARGIN_LEFT + j * CELL_SIZE - CELL_SIZE // 4,
                MARGIN_TOP + i * CELL_SIZE - CELL_SIZE // 4,
                MARGIN_LEFT + j * CELL_SIZE + (CELL_SIZE // 4),
                MARGIN_TOP + i * CELL_SIZE + (CELL_SIZE // 4),
                outline='green',  # fill='red',
                tags='candidate')
            self.candidates[item] = i, j

    def move_piece(self, e):
        def _distance(c):
            left, top, right, bottom = self.canvas.coords(c)
            x1, y1 = (left + right) // 2, (top + bottom) // 2
            return math.sqrt((e.x-x1) ** 2 + (e.y-y1) ** 2)
        c = min(self.canvas.find_withtag('candidate'), key=_distance)
        row, col, _ = self.pieces[self.piece_to_move[0]]
        if _distance(c) > CELL_SIZE:
            self.board_state.move((row, col), (row, col))
        else:
            self.board_state.change_turn()
            self.board_state.move((row, col), self.candidates[c])

b = JanggiBoard()
b.canvas.pack(expand=TRUE, fill=BOTH)

root.mainloop()
