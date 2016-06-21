# coding: utf-8

from tkinter import Tk

from .janggi_board import JanggiBoard
import sys

formations = ['left', 'right', 'inside', 'right']

def check_arguments(argv):
    if len(sys.argv) != 3:
        return False
    return (sys.argv[1] in formations) and (sys.argv[2] in formations)

if check_arguments(sys.argv):
    root = Tk()

    root.title(u'조선장기')
    root.bind('<Escape>', lambda e: root.quit())

    b = JanggiBoard(root)
    b.init_gui(sys.argv[1], sys.argv[2])

    root.mainloop()
else:
    print("Usage: ./run.sh formation1 formation2")
    print("   formation1: formation for a(han, red)")
    print("   formation2: formation for b(cho, blue)")
    print("   formation type: [left|right|inside|outside]")
