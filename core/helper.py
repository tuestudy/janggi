# -*- encoding: utf-8 -*-
from data import code2name, MAX_ROW, MAX_COL


def create_empty_board():
    return [[0] * 9 for _ in range(10)]


def board_state(board):
    return 'A\n' + '\n'.join(' '.join(map(lambda c: '[%7s]' % code2name(c), row)) for row in board) + '\nB\n'


def is_valid_position(row, col):
    return 0 <= row <= MAX_ROW and 0 <= col <= MAX_COL
