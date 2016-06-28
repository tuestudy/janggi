# -*- encoding: utf-8 -*-

import enum
from data import Piece

# Formation
#   * left_sang 왼상차림, 상마상마
#   * right_sang 오른상차림, 마상마상
#   * inside_sang 안상차림  (default), 마상상마
#   * outside_sang 바깥상차림, 상마마상


class FormationType(enum.IntEnum):
    InsideSang, OutsideSang, LeftSang, RightSang = range(4)

A_INITIAL_STATE = [
    (0, 0, Piece.Cha_a),
    (0, 1, Piece.Ma_a),
    (0, 2, Piece.Sang_a),
    (0, 3, Piece.Sa_a),
    (0, 5, Piece.Sa_a),
    (0, 6, Piece.Sang_a),
    (0, 7, Piece.Ma_a),
    (0, 8, Piece.Cha_a),
    (1, 4, Piece.Kung_a),
    (2, 1, Piece.Po_a),
    (2, 7, Piece.Po_a),
    (3, 0, Piece.Jol_a),
    (3, 2, Piece.Jol_a),
    (3, 4, Piece.Jol_a),
    (3, 6, Piece.Jol_a),
    (3, 8, Piece.Jol_a),
]

B_INITIAL_STATE = [
    (9, 0, Piece.Cha_b),
    (9, 1, Piece.Ma_b),
    (9, 2, Piece.Sang_b),
    (9, 3, Piece.Sa_b),
    (9, 5, Piece.Sa_b),
    (9, 6, Piece.Sang_b),
    (9, 7, Piece.Ma_b),
    (9, 8, Piece.Cha_b),
    (8, 4, Piece.Kung_b),
    (7, 1, Piece.Po_b),
    (7, 7, Piece.Po_b),
    (6, 0, Piece.Jol_b),
    (6, 2, Piece.Jol_b),
    (6, 4, Piece.Jol_b),
    (6, 6, Piece.Jol_b),
    (6, 8, Piece.Jol_b),
]


def get_formation(formation_type, init_state, turn):
    formation = list(init_state)
    if turn == 'a':
        baseline = 0
        sang = Piece.Sang_a
        ma = Piece.Ma_a
    else:
        baseline = 9
        sang = Piece.Sang_b
        ma = Piece.Ma_b
    if formation_type == FormationType.OutsideSang:  # 상마마상
        formation[1] = (baseline, 1, sang)
        formation[2] = (baseline, 2, ma)
        formation[5] = (baseline, 6, ma)
        formation[6] = (baseline, 7, sang)
    elif ((turn == 'a' and formation_type == FormationType.LeftSang)
          or (turn == 'b' and formation_type == FormationType.RightSang)):
        formation[5] = (baseline, 6, ma)
        formation[6] = (baseline, 7, sang)
    elif ((turn == 'a' and formation_type == FormationType.RightSang)
          or (turn == 'b' and formation_type == FormationType.LeftSang)):
        formation[1] = (baseline, 1, sang)
        formation[2] = (baseline, 2, ma)
    return formation    # 마상마상


def get_A_formation(formation_type=FormationType.InsideSang):
    return get_formation(formation_type, A_INITIAL_STATE, 'a')


def get_B_formation(formation_type=FormationType.InsideSang):
    return get_formation(formation_type, B_INITIAL_STATE, 'b')
