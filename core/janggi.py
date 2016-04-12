#-*- encoding: utf-8 -*-
from data import A_INITIAL_STATE, B_INITIAL_STATE, CODE_NAMES, code2name, name2code
from helper import create_empty_board, board_state


EMPTY = 0

class Janggi(object):
    def __init__(self):
        self.board = [[EMPTY]*9 for _ in range(10)]

    def __repr__(self):
        return board_state(self.board)

    def reset(self):
        self.board = create_empty_board()
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

    def move(self, old_pos, new_pos):
        row1, col1 = old_pos
        row2, col2 = new_pos
        assert self.board[row1][col1] != EMPTY
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = EMPTY

    def delete(self, pos):
        row, col = pos
        assert self.board[row][col] != EMPTY
        self.board[row][col] = EMPTY


if '__main__' == __name__:
    janggi = Janggi()
    janggi.reset()
    print(janggi)
