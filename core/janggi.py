#-*- encoding: utf-8 -*-
from data import A_INITIAL_STATE, B_INITIAL_STATE, CODE_NAMES, code2name, name2code
from helper import create_empty_board, board_state
from rx.subjects import Subject

class Janggi(object):
    def __init__(self):
        self.boardState = Subject()
        self._board = None

        self.board = [[0]*9 for _ in range(10)]

    def __repr__(self):
        return board_state(self.board)

    def reset(self):
        self.board = create_empty_board()
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

    def _emit_board_state(self):
        self.boardState.on_next(self._board)

    def _get_board(self):
        return self._board

    def _set_board(self, value):
        self._board = value
        self._emit_board_state()

    board = property(_get_board, _set_board, None, "")

if '__main__' == __name__:
    janggi = Janggi()
    janggi.boardState.subscribe(lambda state:
        print(janggi)
    )

    janggi.reset()
    janggi.reset()
    janggi.reset()
    janggi.reset()
