# -*- encoding: utf-8 -*-
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
    def __init__(
            self,
            change_callback=None,
            turn_change_callback=None):
        self.board = [[EMPTY] * 9 for _ in range(10)]
        self.on_changed = change_callback
        self.on_turn_changed = turn_change_callback
        self.turn = 'b'  # b(楚) -> a(漢) -> b -> a -> ..
        self.first_mover = self.turn

    def __repr__(self):
        return board_state(self.board)

    def broadcast(self):
        if self.on_changed is not None:
            self.on_changed(self.board)

    def exist(self, pos):
        row, col = pos
        return self.board[row][col] != EMPTY

    def change_turn(self):
        self.turn = {'a': 'b', 'b': 'a'}[self.turn]
        if self.on_turn_changed:
            self.on_turn_changed(self.turn)

    def can_move(self, piece):
        return piece.team == self.turn

    @broadcasted
    def reset(self, han_formation, cho_formation):
        self.board = create_empty_board()
        for row, col, code in han_formation + cho_formation:
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
        self.change_turn()

    def score(self, player):
        s = sum(piece.score
                for row in self.board
                for piece in row
                if piece and piece.team == player)
        if player != self.first_mover:
            # 후수자 덤
            s += 1.5
        return s

if '__main__' == __name__:
    def change_callback(board):
        print(janggi)

    janggi = Janggi(change_callback)
    janggi.reset()

    janggi.move((0, 0), (1, 0))
    janggi.delete((1, 0))
