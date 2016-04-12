#-*- encoding: utf-8 -*-
import enum

MAX_ROW = 9
MAX_COL = 8

"""
  졸/병이 움직이는 방향을 정할 때 진영 정보가 필요함
  * A 가 상단(Row 가 작은 쪽)
  * B 가 하단(Row 가 큰 쪽)
"""

class PieceType(enum.IntEnum):
    Kung, Cha, Po, Ma, Sang, Sa, Byung, Jol = range(1, 9)

class Piece(enum.IntEnum):
    __ = 0
    Kung_a, Cha_a, Po_a, Ma_a, Sang_a, Sa_a, Byung_a = range(1, 8)
    Kung_b, Cha_b, Po_b, Ma_b, Sang_b, Sa_b, Jol_b = range(8, 15)

CODE_NAMES = [p.name.replace('_', '-') if p else p.name for p in Piece]
for p in Piece:
    if p:
        p.team = p.name[-1]

Piece.Kung_a.piece_type = PieceType.Kung
Piece.Kung_b.piece_type = PieceType.Kung
Piece.Cha_a.piece_type = PieceType.Cha
Piece.Cha_b.piece_type = PieceType.Cha
Piece.Po_a.piece_type = PieceType.Po
Piece.Po_b.piece_type = PieceType.Po
Piece.Ma_a.piece_type = PieceType.Ma
Piece.Ma_b.piece_type = PieceType.Ma
Piece.Sang_a.piece_type = PieceType.Sang
Piece.Sang_b.piece_type = PieceType.Sang
Piece.Byung_a.piece_type = PieceType.Byung
Piece.Jol_b.piece_type = PieceType.Jol
Piece.Sa_a.piece_type = PieceType.Sa
Piece.Sa_b.piece_type = PieceType.Sa


assert len(CODE_NAMES) == 7 + 7 + 1

def is_valid_code(c):
    try:
        Piece(c)
        return True
    except ValueError:
        return False
 
def is_valid_coordinates(r, c):
    return 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL

def code2name(c):
    try:
        name = Piece(c).name
        return name.replace('_', '-') if c else name
    except ValueError:
        return 'X'

def name2code(name):
    return getattr(Piece, name.replace('-', '_')).value


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
    (3, 0, Piece.Byung_a),
    (3, 2, Piece.Byung_a),
    (3, 4, Piece.Byung_a),
    (3, 6, Piece.Byung_a),
    (3, 8, Piece.Byung_a),
]

B_INITIAL_STATE = [
    (9, 0, Piece.Cha_b),
    (9, 1, Piece.Sang_b),
    (9, 2, Piece.Ma_b),
    (9, 3, Piece.Sa_b),
    (9, 5, Piece.Sa_b),
    (9, 6, Piece.Ma_b),
    (9, 7, Piece.Sang_b),
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

MOVES = {
    PieceType.Kung : [
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1,  1), ( 1,  0), ( 1, -1)
              ],
    PieceType.Sa   : [
        (-1, -1), (-1,  0), (-1,  1),
        ( 0, -1),           ( 0,  1),
        ( 1,  1), ( 1,  0), ( 1, -1)
              ],
    PieceType.Sang : [
            (-3, -2), (-3,  2),
        (-2, -3),        (-2,  3),
        ( 2, -3),        ( 2,  3),
            ( 3, -2), ( 3,  2)
              ],
    PieceType.Ma   : [
            (-1, -2), (-1,  2),
        (-2, -1),        (-2,  1),
        ( 1, -2),        ( 1,  2),
            ( 2, -1), ( 2,  1)
              ],
    PieceType.Byung: [
                  ( 1,  0),
        ( 0, -1),            ( 0,  1)
              ],
    PieceType.Jol:   [
                  (-1,  0),
        ( 0, -1),            ( 0,  1)
              ]
}
MOVES = {pt.name: moves for pt, moves in MOVES.items()}


