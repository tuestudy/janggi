import pytest

from data import Piece
from janggi import Janggi
from rule import next_possible_coordinates


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
