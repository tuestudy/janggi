#-*- encoding: utf-8 -*-
from data import A_INITIAL_STATE, B_INITIAL_STATE, CODE_NAMES, code2name, name2code, is_valid_coordinates
from helper import create_empty_board, board_state
from rule import next_possible_coordinates


class Janggi(object):
    def __init__(self):
        self.board = [[0]*9 for _ in range(10)]
        self.on_changed = None

    def __repr__(self):
        return board_state(self.board)

    def reset(self):
        self.board = create_empty_board()
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

    def move(self, from_position, to_position):
        from_row, from_col = from_position
        to_row, to_col = to_position
        assert(is_valid_coordinates(from_row, from_col))
        assert(is_valid_coordinates(to_row, to_col))
        assert(self.board[from_row][from_col] != 0)
        assert(self.board[to_row][to_col] == 0)

        assert(to_position in self.movable_positions(from_position))

        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = 0
        self.broadcast()

    def movable_positions(self, from_position):
        from_row, from_col = from_position
        assert(is_valid_coordinates(from_row, from_col))
        code = self.board[from_row][from_col]
        assert(code != 0)
        return next_possible_coordinates(from_row, from_col, code)

    def broadcast(self):
        if self.on_changed is not None:
            self.on_changed(self.board)

if '__main__' == __name__:
    janggi = Janggi()
    janggi.reset()
    print(janggi)

    def change_callback(board):
        print(janggi)

    janggi.on_changed = change_callback
    janggi.move((0, 0), (1, 0))
