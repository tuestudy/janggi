import pytest

from data import Piece
from janggi import Janggi
from rule import next_coordinates, next_possible_coordinates


@pytest.fixture(scope='function')
def empty_board():
    return Janggi().board


def test_cha_mobility(empty_board):
    coords = set(next_possible_coordinates(empty_board, 1, 1, Piece.Cha_a))

    up = {(0, 1)}
    down = {(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)}
    left = {(1, 0)}
    right = {(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)}
    assert coords == left | right | up | down


def test_byung_mobility(empty_board):
    coords = set(next_possible_coordinates(empty_board, 2, 2, Piece.Byung_a))

    down, left, right = (3, 2), (2, 1), (2, 3)
    assert coords == {down, left, right}


def test_jol_mobility(empty_board):
    coords = set(next_possible_coordinates(empty_board, 6, 2, Piece.Jol_b))

    up, left, right = (5, 2), (6, 1), (6, 3)
    assert coords == {up, left, right}


def check_mobility(spec):
    """
    @param spec - 다음의 문자(열)로 구성된 문자열
        o       - 움직일 기물
        대문자  - 갈 수 있는곳
        소문자  - 갈 수 없는곳
        .       - 빈칸 (갈 수 없는곳)
        공백    - 무시됨
        줄바꿈  - 행구분
        c=Cha_a - 사용된 문자와 기물 매핑
    """

    rows = [row for row in spec.strip().splitlines()]
    board = [row.split()[0] for row in rows]
    piece_mapping = {
        char: getattr(Piece, name)
        for char, name in (
            m.split('=')
            for row in rows
            for m in row.split()[1:]
        )
    }
    janggi = Janggi()

    pos = piece = None
    possible_positions = set()
    for i, row in enumerate(board):
        for j, x in enumerate(row):
            p = piece_mapping.get(x, 0)
            if x == 'o':
                assert not pos, 'x should be specified once'
                pos = i, j
                piece = p
            elif x.isupper():
                possible_positions.add((i, j))
            janggi.board[i][j] = p
    assert pos, 'x should be specified once'
    coords = set(next_coordinates(janggi.board, *pos, piece))
    assert coords == possible_positions


def test_cha_cannot_pass_enemy():
    check_mobility('''
        .........
        ....q....  q=Kung_a
        .........
        .........
        ........A  B=Cha_a
        XXXXXXXXo  o=Cha_b
        ........X
        ........X
        ....k...X  k=Kung_b
        ........X
    ''')
