#-*- encoding: utf-8 -*-
from data import A_INITIAL_STATE, B_INITIAL_STATE, is_valid_coordinates
from helper import create_empty_board, board_state
from rule import next_coordinates

EMPTY = 0

def broadcasted(func, ):
    def _func(*args, **kwargs):
        func(*args, **kwargs)
        self = args[0]
        self.broadcast()
    return _func

class Janggi(object):
    def __init__(self, change_callback=None):
        self.board = [[EMPTY]*9 for _ in range(10)]
        self.on_changed = change_callback

    def __repr__(self):
        return board_state(self.board)

    def broadcast(self):
        if self.on_changed is not None:
            self.on_changed(self.board)

    def exist(self, pos):
        row, col = pos
        return self.board[row][col] != EMPTY

    @broadcasted
    def reset(self):
        self.board = create_empty_board()
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

    @broadcasted
    def move(self, old_pos, new_pos):
        assert self.exist(old_pos)
        if old_pos == new_pos:
            return
        row1, col1 = old_pos
        row2, col2 = new_pos
        code = self.board[row1][col1]
        assert(new_pos in next_coordinates(self.board, row1, col1, code))
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = EMPTY

    @broadcasted
    def delete(self, pos):
        assert self.exist(pos)
        row, col = pos
        self.board[row][col] = EMPTY

if '__main__' == __name__:
    def change_callback(board):
        print(janggi)

    janggi = Janggi(change_callback)
    janggi.reset()

    janggi.move((0, 0), (1, 0))
    janggi.delete((1, 0))
