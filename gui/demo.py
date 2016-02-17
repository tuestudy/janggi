# coding: utf-8

from pathlib import Path
from tkinter import *  # noqa

from PIL import ImageTk

from ..core.data import Piece
from ..core.janggi import Janggi


HORIZONTAL_LINES = 10
VERTICAL_LINES = 9
MARGIN_TOP = MARGIN_LEFT = 50
CELL_SIZE = 100
BOARD_WIDTH = CELL_SIZE * (VERTICAL_LINES - 1)
BOARD_HEIGHT = CELL_SIZE * (HORIZONTAL_LINES - 1)
CANVAS_WIDTH = BOARD_WIDTH + 2 * MARGIN_LEFT
CANVAS_HEIGHT = BOARD_HEIGHT + 2 * MARGIN_TOP

janggi = Janggi()
janggi.reset()

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


class ScrollableCanvas(Frame):

    def __init__(self, master, width, height, *args, **kwargs):
        Frame.__init__(self, master, bd=2, relief=SUNKEN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        xscrollbar.grid(row=1, column=0, sticky=E+W)
        yscrollbar = Scrollbar(self)
        yscrollbar.grid(row=0, column=1, sticky=N+S)
        canvas = self.canvas = Canvas(
            self, *args, bd=0,
            xscrollcommand=xscrollbar.set,
            yscrollcommand=yscrollbar.set,
            width=width, height=height,
            **kwargs)
        canvas.grid(row=0, column=0, sticky=N+S+E+W)
        canvas.config(scrollregion=(0, 0, width, height))
        canvas.bind_all('<MouseWheel>', self.on_vertical_scroll)
        canvas.bind_all('<Button-4>', self.on_vertical_scroll)
        canvas.bind_all('<Button-5>', self.on_vertical_scroll)
        canvas.bind_all('<Shift-MouseWheel>', self.on_horizontal_scroll)
        canvas.bind_all('<Shift-Button-4>', self.on_horizontal_scroll)
        canvas.bind_all('<Shift-Button-5>', self.on_horizontal_scroll)
        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)

    @staticmethod
    def scroll_direction(event):
        return -1 if event.num == 4 or event.delta > 0 else +1

    def on_vertical_scroll(self, event):
        self.canvas.yview_scroll(self.scroll_direction(event), 'units')

    def on_horizontal_scroll(self, event):
        self.canvas.xview_scroll(self.scroll_direction(event), 'units')


root = Tk()

photoimages = {
    piece: ImageTk.PhotoImage(file=resource_dir / (filename + '.png'))
    for piece, filename in images.items()
}
sc = ScrollableCanvas(root, CANVAS_WIDTH, CANVAS_HEIGHT, background='#F7931E')
sc.pack(expand=TRUE, fill=BOTH)
canvas = sc.canvas

# hotizontal lines
for i in range(HORIZONTAL_LINES):
    y = MARGIN_TOP + i * CELL_SIZE
    canvas.create_line(MARGIN_LEFT, y, MARGIN_LEFT + BOARD_WIDTH, y)
# vertical lines
for i in range(VERTICAL_LINES):
    x = MARGIN_LEFT + i * CELL_SIZE
    canvas.create_line(x, MARGIN_TOP, x, MARGIN_TOP + BOARD_HEIGHT)

# palaces
for i in (0, 7):
    y = MARGIN_TOP + i * CELL_SIZE
    canvas.create_line(
        MARGIN_LEFT + 3 * CELL_SIZE,
        y,
        MARGIN_LEFT + 5 * CELL_SIZE,
        y + 2 * CELL_SIZE)
    canvas.create_line(
        MARGIN_LEFT + 5 * CELL_SIZE,
        y,
        MARGIN_LEFT + 3 * CELL_SIZE,
        y + 2 * CELL_SIZE)

# pieces
for i, row in enumerate(janggi.board):
    for j, piece in enumerate(row):
        if not piece:
            continue
        canvas.create_image(
            MARGIN_LEFT + j * CELL_SIZE,
            MARGIN_TOP + i * CELL_SIZE,
            image=photoimages[piece])

root.geometry('{}x{}'.format(CANVAS_WIDTH, CANVAS_HEIGHT))
root.title(u'조선장기')
root.mainloop()
