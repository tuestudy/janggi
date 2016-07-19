# coding: utf-8

import argparse
from tkinter import Tk

from .janggi_board import JanggiBoard

formations = ['left', 'right', 'inside', 'outside']


parser = argparse.ArgumentParser(description='조선장기')
parser.add_argument(
    '-a', '--red-formation', choices=formations, type=str,
    default='inside', help='초 상차림')
parser.add_argument(
    '-b', '--green-formation', choices=formations, type=str,
    default='inside', help='한 상차림')
parser.add_argument(
    '-c', '--custom-formation', metavar='file path',
    type=argparse.FileType('r'),
    help='custom formation - specify file path')

args = parser.parse_args()
if args.custom_formation:
    f = args.custom_formation
    args.custom_formation = f.read()
    f.close()

root = Tk()

root.title(u'조선장기')
root.bind('<Escape>', lambda e: root.quit())
root.wm_attributes("-topmost", 1)
root.after(1000, root.wm_attributes, "-topmost", 0)

board = JanggiBoard(root)
board.init_gui(args.red_formation, args.green_formation, args.custom_formation)

root.mainloop()
