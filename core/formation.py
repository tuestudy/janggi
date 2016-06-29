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

In, Out, Left, Right = FormationType


initial_states = {
    'a': [
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
    ],
    'b': [
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
}

sang_ma_layouts = {
    'a': {
        Out:   [Piece.Sang_a, Piece.Ma_a, Piece.Ma_a, Piece.Sang_a],
        In:    [Piece.Ma_a, Piece.Sang_a, Piece.Sang_a, Piece.Ma_a],
        Right: [Piece.Sang_a, Piece.Ma_a, Piece.Sang_a, Piece.Ma_a],
        Left:  [Piece.Ma_a, Piece.Sang_a, Piece.Ma_a, Piece.Sang_a],
    },
    'b': {
        Out:   [Piece.Sang_b, Piece.Ma_b, Piece.Ma_b, Piece.Sang_b],
        In:    [Piece.Ma_b, Piece.Sang_b, Piece.Sang_b, Piece.Ma_b],
        Right: [Piece.Ma_b, Piece.Sang_b, Piece.Ma_b, Piece.Sang_b],
        Left:  [Piece.Sang_b, Piece.Ma_b, Piece.Sang_b, Piece.Ma_b],
    },
}

baselines = {
    'a': 0,
    'b': 9,
}


def get_formation(team, formation_type=FormationType.InsideSang):
    baseline = baselines[team]
    layout = sang_ma_layouts[team][formation_type]
    formation = list(initial_states[team])
    for i, j, piece in zip((1, 2, 5, 6), (1, 2, 6, 7), layout):
        formation[i] = baseline, j, piece
    return formation
