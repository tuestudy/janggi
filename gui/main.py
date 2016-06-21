# coding: utf-8

from tkinter import Tk

from .janggi_board import JanggiBoard
import sys

formations = ['left', 'right', 'inside', 'outside']

def check_arguments(argv):
    return ((len(sys.argv) == 3)
            and (sys.argv[1] in formations)
            and (sys.argv[2] in formations))

def print_usage():
    print("사용법: ./run.sh [formation1] [formation2]")
    print("   formation1: 한나라의 상차림")
    print("   formation2: 초나라의 상차림")
    print("   상자림 유형: [left|right|inside|outside]")

if len(sys.argv) == 1:
    print("상차림이 지정되지 않았습니다. 기본 상차림을 사용합니다.")
    a = b = 'left'
elif check_arguments(sys.argv):
    a, b = sys.argv[1], sys.argv[2]
else:
    print_usage()
    sys.exit()

root = Tk()

root.title(u'조선장기')
root.bind('<Escape>', lambda e: root.quit())

board = JanggiBoard(root)
board.init_gui(a, b)

root.mainloop()
