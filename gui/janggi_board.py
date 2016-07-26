# coding: utf-8

from math import hypot
from pathlib import Path
from collections import namedtuple

from PIL import ImageTk, Image
from tkinter import Button, Label, Canvas

from ..core.data import Piece, NUM_ROW, NUM_COL
from ..core.janggi import Janggi
from ..core.rule import next_coordinates
from ..core.formation import FormationType, get_formation, parse

HORIZONTAL_LINES = NUM_ROW
VERTICAL_LINES = NUM_COL
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
    Piece.Jol_a: 'Red_Jol',
    Piece.Jol_b: 'Green_Zol',
    Piece.Sa_a: 'Red_Sa',
    Piece.Sa_b: 'Green_Sa',
}

PieceInfo = namedtuple('PieceInfo', ('row', 'col', 'name', 'item'))


class JanggiBoard:

    def __init__(self, master, *args, **kwargs):
        self.photoimages = {
            piece: ImageTk.PhotoImage(Image.open(
                resource_dir / (filename + '.png')
            ).resize((60, 54)))
            for piece, filename in images.items()
        }
        for name in ['boom', 'red_win', 'green_win']:
            self.photoimages[name] = ImageTk.PhotoImage(Image.open(
                resource_dir / (name + '.png')))
        self.canvas = Canvas(
            master=master,
            width=CANVAS_HEIGHT, height=CANVAS_HEIGHT,
            background=BOARD_COLOR, *args, **kwargs
        )
        self.change_turn_button = Button(
            master=master,
            text='한수쉼',
            command=self.on_change_turn_button_pressed,
        )

        self.label_colors = {'a': 'red', 'b': 'blue', 'default': master['bg']}
        self.turn_0_label = Label(master=master, text="       ")
        self.turn_1_label = Label(master=master, text="       ",
                                  bg=self.label_colors['b'])

        self.draw_hlines()
        self.draw_vlines()
        self.draw_palaces()
        self.canvas.bind('<Button-1>', self.on_button_pressed)
        self.canvas.bind('<ButtonRelease-1>', self.on_button_released)
        self.canvas.bind('<Button1-Motion>', self.on_button_motion)
        self.board_state = Janggi(
            lambda x: self.update_canvas(),
            turn_change_callback=self.on_turn_changed,
            gameover_callback=self.on_gameover)
        self.gameover = False

    def init_gui(self, formation_a, formation_b, customer_formation):
        self.canvas.grid(row=0, column=0, rowspan=3)
        self.turn_0_label.grid(row=0, column=1)
        self.change_turn_button.grid(row=1, column=1)
        self.turn_1_label.grid(row=2, column=1)
        if customer_formation:
            _, formation, _ = parse(customer_formation)
            self.board_state.reset(formation, [])
        else:
            self.board_state.reset(
                get_formation('a', FormationType[formation_a]),
                get_formation('b', FormationType[formation_b]))

    def draw_hlines(self):
        for i in range(HORIZONTAL_LINES):
            y = MARGIN_TOP + i * CELL_SIZE
            self.canvas.create_line(MARGIN_LEFT, y,
                                    MARGIN_LEFT + BOARD_WIDTH, y)

    def draw_vlines(self):
        for i in range(VERTICAL_LINES):
            x = MARGIN_LEFT + i * CELL_SIZE
            self.canvas.create_line(x, MARGIN_TOP,
                                    x, MARGIN_TOP + BOARD_HEIGHT)

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

    def put_pieces(self):
        d = self.pieces = {}  # Map canvas item -> PieceInfo(row, col, piece)
        for i, row in enumerate(self.board_state.board):
            for j, piece in enumerate(row):
                if not piece:
                    continue
                item = self.canvas.create_image(
                    MARGIN_LEFT + j * CELL_SIZE,
                    MARGIN_TOP + i * CELL_SIZE,
                    image=self.photoimages[piece],
                    tags='piece')
                d[item] = PieceInfo(row=i, col=j, name=piece, item=item)

    def update_canvas(self):
        self.current_piece = None
        self.canvas.delete('piece')
        self.candidates = {}
        self.canvas.delete('candidate')
        self.put_pieces()

    def get_current_piece(self):
        item = self.canvas.find_withtag('current')
        if not item:
            return None
        if 'piece' not in self.canvas.gettags(item[0]):
            return None
        current_piece = self.pieces[item[0]]
        if not self.board_state.can_move(current_piece.name):
            return None
        return current_piece

    def on_button_pressed(self, e):
        self.current_piece = self.get_current_piece()
        if self.current_piece:
            self.x, self.y = e.x, e.y
            self.show_candidates(e)

    def on_button_released(self, e):
        if self.current_piece:
            self.move_piece(e)

    def on_button_motion(self, e):
        if self.current_piece:
            self.canvas.move(self.current_piece.item,
                             e.x - self.x, e.y - self.y)
            self.x, self.y = e.x, e.y

    def on_change_turn_button_pressed(self):
        self.board_state.change_turn()

    def on_turn_changed(self, turn):
        if turn == 'a':
            self.turn_0_label.configure(bg=self.label_colors[turn])
            self.turn_1_label.configure(bg=self.label_colors['default'])
        else:
            self.turn_0_label.configure(bg=self.label_colors['default'])
            self.turn_1_label.configure(bg=self.label_colors[turn])

    def on_gameover(self, last_kung_pos, winner):
        i, j = last_kung_pos
        self._gameover_image = self.canvas.create_image(
            MARGIN_LEFT + j * CELL_SIZE,
            MARGIN_TOP + i * CELL_SIZE,
            image=self.photoimages['boom'])
        if winner == 'a':
            win_image = 'red_win'
        else:
            win_image = 'green_win'
        self._gameover_image = self.canvas.create_image(
            MARGIN_LEFT + 4 * CELL_SIZE,
            MARGIN_TOP + 5 * CELL_SIZE,
            image=self.photoimages[win_image])
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.unbind('<Button1-Motion>')

    def show_candidates(self, e):
        r, c, p, pi = self.current_piece
        self.canvas.tag_raise(pi)
        self.candidates = {}
        coords = [(r, c)] + next_coordinates(self.board_state.board, r, c, p)
        for i, j in coords:
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
            return hypot((e.x - x1), (e.y - y1))
        old_pos = (self.current_piece.row, self.current_piece.col)
        candidates = self.canvas.find_withtag('candidate')
        if candidates:
            c = min(candidates, key=_distance)
            new_pos = (self.candidates[c] if _distance(c) < CELL_SIZE else
                       old_pos)
        else:
            new_pos = old_pos
        self.board_state.move(old_pos, new_pos)
