#-*- encoding: utf-8 -*-
from data import A_INITIAL_STATE, B_INITIAL_STATE, CODE_NAMES, code2name, name2code
from helper import create_empty_board, board_state


class Janggi(object):
    def __init__(self):
        self.board = [[0]*9 for _ in range(10)]

    def __repr__(self):
        return board_state(self.board)

    def reset(self):
        self.board = create_empty_board()
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

if '__main__' == __name__:
    janggi = Janggi()
    janggi.reset()
    print(janggi)
