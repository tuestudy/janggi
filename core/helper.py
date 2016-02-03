#-*- encoding: utf-8 -*-
from data import code2name

def create_empty_board():
    return [[0]*9 for _ in range(10)]


def board_state(board):
    return 'A\n' + '\n'.join(' '.join(map(lambda c: '[%7s]' %code2name(c), row)) for row in board) + '\nB\n'
