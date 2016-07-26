# -*- encoding: utf-8 -*-
import enum

NUM_ROW = 10
NUM_COL = 9

"""
  졸/병이 움직이는 방향을 정할 때 진영 정보가 필요함
  * A 가 상단(Row 가 작은 쪽) 漢
  * B 가 하단(Row 가 큰 쪽) 楚
"""


class PieceType(enum.IntEnum):
    Empty, Kung, Cha, Po, Ma, Sang, Sa, Jol = range(0, 8)

    @property
    def piece_type(self):
        # XXX
        return self

PieceType.Kung.score = 0
PieceType.Cha.score = 13
PieceType.Po.score = 7
PieceType.Ma.score = 5
PieceType.Sang.score = 3
PieceType.Sa.score = 3
PieceType.Jol.score = 2


class Piece(enum.IntEnum):
    Empty = 0
    Kung_a, Cha_a, Po_a, Ma_a, Sang_a, Sa_a, Jol_a = range(1, 8)
    Kung_b, Cha_b, Po_b, Ma_b, Sang_b, Sa_b, Jol_b = range(8, 15)

    @property
    def score(self):
        return self.piece_type.score

    @property
    def team(self):
        return self.name[-1]

    @property
    def piece_type(self):
        t = self.name.split('_')[0]
        return PieceType[t]


CODE_NAMES = [p.name.replace('_', '-') if p else p.name for p in Piece]
assert len(CODE_NAMES) == 7 + 7 + 1


def is_valid_coordinates(r, c):
    return 0 <= r < NUM_ROW and 0 <= c < NUM_COL


def code2name(c):
    try:
        name = Piece(c).name
        return name.replace('_', '-') if c else name
    except ValueError:
        return 'X'


MOVES = {
    PieceType.Kung: [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, 1), (1, 0), (1, -1)
    ],
    PieceType.Sa: [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, 1), (1, 0), (1, -1)
    ],
    PieceType.Sang: [
        (-3, -2), (-3, 2),
        (-2, -3), (-2, 3),
        (2, -3), (2, 3),
        (3, -2), (3, 2)
    ],
    PieceType.Ma: [
        (-1, -2), (-1, 2),
        (-2, -1), (-2, 1),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ],
    Piece.Jol_b: [
        (-1, 0),
        (0, -1), (0, 1)
    ],
    Piece.Jol_a: [
        (1, 0),
        (0, -1), (0, 1)
    ],
}
