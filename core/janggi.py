# -*- encoding: utf-8 -*-
from data import Piece, PieceType, NUM_ROW, NUM_COL
from helper import board_state
from rule import next_coordinates


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
            turn_change_callback=None,
            gameover_callback=None):
        self.clear()
        self.on_changed = change_callback
        self.on_turn_changed = turn_change_callback
        self.on_gameover = gameover_callback
        self.turn = 'b'  # b(楚) -> a(漢) -> b -> a -> ..
        self.first_mover = self.turn
        self.gameover = False
        self.winner = None
        self.last_position = None

    def __repr__(self):
        return board_state(self.board)

    def broadcast(self):
        if self.on_changed is not None:
            self.on_changed(self.board)
        if self.gameover and self.on_gameover:
            self.on_gameover(self.last_position, self.winner)

    def exist(self, pos):
        row, col = pos
        return self.board[row][col]

    def change_turn(self):
        self.turn = {'a': 'b', 'b': 'a'}[self.turn]
        if self.on_turn_changed:
            self.on_turn_changed(self.turn)

    def game_over(self):
        if self.on_gameover:
            self.on_gameover(self.last_position, self.winner)

    def can_move(self, piece):
        return piece.team == self.turn

    def clear(self):
        self.board = [[Piece.Empty] * NUM_COL for _ in range(NUM_ROW)]

    @broadcasted
    def reset(self, han_formation, cho_formation):
        self.clear()
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
        assert new_pos in next_coordinates(self.board, row1, col1, code)
        if self.board[row2][col2].piece_type == PieceType.Kung:
            self.gameover = True
            self.last_position = row2, col2
            self.winner = self.turn
        self.last_handle_postion = new_pos
        self.board[row2][col2] = self.board[row1][col1]
        self.board[row1][col1] = Piece.Empty
        if self.gameover:
            self.game_over()
        else:
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
