# coding: utf-8

from tkinter import Tk

from .janggi_board import JanggiBoard

root = Tk()

root.title(u'조선장기')
root.bind('<Escape>', lambda e: root.quit())

b = JanggiBoard()
b.init_gui()

root.mainloop()
