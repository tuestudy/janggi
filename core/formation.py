#-*- encoding: utf-8 -*-

import enum
from data import Piece

# Formation
#   * left_sang 왼상차림
#   * right_sang 오른상차림
#   * inside_sang 안상차림  (default)
#   * outside_sang 바깥상차림

class FormationType(enum.IntEnum):
    InsideSang, OutsideSang, LeftSang, RightSang = range(4)

HAN_INITIAL_STATE = [
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
    (3, 0, Piece.Byung_a),
    (3, 2, Piece.Byung_a),
    (3, 4, Piece.Byung_a),
    (3, 6, Piece.Byung_a),
    (3, 8, Piece.Byung_a),
]

CHO_INITIAL_STATE = [
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


def get_han_formation(formation_type):
    formation = list(HAN_INITIAL_STATE)
    if formation_type == FormationType.OutsideSang:
        formation[1] = (0, 1, Piece.Sang_a)
        formation[2] = (0, 2, Piece.Ma_a)
        formation[5] = (0, 6, Piece.Ma_a)
        formation[6] = (0, 7, Piece.Sang_a)
    return formation

def get_cho_formation(formation_type):
    formation = list(CHO_INITIAL_STATE)
    if formation_type == FormationType.OutsideSang:
        formation[1] = (9, 1, Piece.Sang_b)
        formation[2] = (9, 2, Piece.Ma_b)
        formation[5] = (9, 6, Piece.Ma_b)
        formation[6] = (9, 7, Piece.Sang_b)
    return formation
