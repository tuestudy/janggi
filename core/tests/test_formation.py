import pytest

import janggi
from data import Piece
from formation import FormationType, get_han_formation, get_cho_formation

def test_inside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_han_formation(FormationType.InsideSang),
        get_cho_formation(FormationType.InsideSang))
    assert j.board[0][2] == Piece.Sang_a
    assert j.board[0][6] == Piece.Sang_a
    assert j.board[9][2] == Piece.Sang_b
    assert j.board[9][6] == Piece.Sang_b

def test_ouside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_han_formation(FormationType.OutsideSang),
        get_cho_formation(FormationType.OutsideSang))
    assert j.board[0][1] == Piece.Sang_a
    assert j.board[0][7] == Piece.Sang_a
    assert j.board[9][1] == Piece.Sang_b
    assert j.board[9][7] == Piece.Sang_b
