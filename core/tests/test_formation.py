import janggi
from data import Piece
from formation import FormationType, get_han_formation, get_cho_formation

def check_inside_sang(turn, board):
    if turn == 'a':
        assert board[0][1] == Piece.Ma_a
        assert board[0][2] == Piece.Sang_a
        assert board[0][6] == Piece.Sang_a
        assert board[0][7] == Piece.Ma_a
    else:
        assert board[9][1] == Piece.Ma_b
        assert board[9][2] == Piece.Sang_b
        assert board[9][6] == Piece.Sang_b
        assert board[9][7] == Piece.Ma_b

def check_outside_sang(turn, board):
    if turn == 'a':
        assert board[0][1] == Piece.Sang_a
        assert board[0][2] == Piece.Ma_a
        assert board[0][6] == Piece.Ma_a
        assert board[0][7] == Piece.Sang_a
    else:
        assert board[9][1] == Piece.Sang_b
        assert board[9][2] == Piece.Ma_b
        assert board[9][6] == Piece.Ma_b
        assert board[9][7] == Piece.Sang_b


def test_inside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_han_formation(FormationType.InsideSang),
        get_cho_formation(FormationType.InsideSang))
    check_inside_sang('a', j.board)
    check_inside_sang('b', j.board)

def test_outside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_han_formation(FormationType.OutsideSang),
        get_cho_formation(FormationType.OutsideSang))
    check_outside_sang('a', j.board)
    check_outside_sang('b', j.board)

def test_inside_sang_x_outside_sang_formation():
    j = janggi.Janggi(None)
    j.reset(get_han_formation(FormationType.InsideSang),
        get_cho_formation(FormationType.OutsideSang))
    check_inside_sang('a', j.board)
    check_outside_sang('b', j.board)
