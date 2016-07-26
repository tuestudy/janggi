# -*- encoding: utf-8 -*-

import enum
from data import Piece, NUM_ROW
from typing import List, Tuple, Set


Row = Col = int


def parse(spec) -> Tuple[Tuple[Row, Col],
                         List[Tuple[Row, Col, Piece]],
                         Set[Tuple[Row, Col]]]:
    spec = spec.strip()
    if spec[0].isdigit():
        spec = '\n'.join(['.........'] * int(spec[0])) + spec[1:]
    rows = [row for row in spec.strip().splitlines()]
    board = [row.split()[0] for row in rows]
    piece_mapping = {}
    for row in rows:
        for m in row.split()[1:]:
            *chars, name = m.split('=')
            p = getattr(Piece, name)
            for char in chars:
                piece_mapping[char] = p
    pos = None
    pieces = []
    movable_coords = set()
    for i, row in enumerate(board):
        for j, x in enumerate(row):
            p = piece_mapping.get(x, 0)
            if p:
                pieces.append((i, j, p))
            if x == 'o':
                assert not pos, 'o should be specified once'
                pos = i, j
            elif x.isupper():
                movable_coords.add((i, j))
    return pos, pieces, movable_coords


# Formation
#   * left_sang 왼상차림, 상마상마
#   * right_sang 오른상차림, 마상마상
#   * inside_sang 안상차림  (default), 마상상마
#   * outside_sang 바깥상차림, 상마마상


class FormationType(enum.IntEnum):
    InsideSang, OutsideSang, LeftSang, RightSang = range(4)
    inside, outside, left, right = range(4)
    Default = left


initial_states = {
    'a': parse('''
        c..s.s..c  c=Cha_a s=Sa_a
        ....k....  k=Kung_a
        .p.....p.  p=Po_a
        j.j.j.j.j  j=Jol_a''')[1],
    'b': parse('''
        6
        j.j.j.j.j  j=Jol_b
        .p.....p.  p=Po_b
        ....k....  k=Kung_b
        c..s.s..c  c=Cha_b s=Sa_b''')[1],
}

In, Out, Left, Right = FormationType
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
    'b': NUM_ROW - 1,
}


def get_formation(team, formation_type=FormationType.Default):
    baseline = baselines[team]
    layout = sang_ma_layouts[team][formation_type]
    return initial_states[team] + [
        (baseline, col, piece) for col, piece in zip((1, 2, 6, 7), layout)
    ]
