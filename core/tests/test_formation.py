import janggi
from data import Piece
from formation import FormationType, get_formation


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


def check_left_sang(turn, board):
    if turn == 'a':
        assert board[0][1] == Piece.Ma_a
        assert board[0][2] == Piece.Sang_a
        assert board[0][6] == Piece.Ma_a
        assert board[0][7] == Piece.Sang_a
    else:
        assert board[9][1] == Piece.Sang_b
        assert board[9][2] == Piece.Ma_b
        assert board[9][6] == Piece.Sang_b
        assert board[9][7] == Piece.Ma_b


def check_right_sang(turn, board):
    if turn == 'a':
        assert board[0][1] == Piece.Sang_a
        assert board[0][2] == Piece.Ma_a
        assert board[0][6] == Piece.Sang_a
        assert board[0][7] == Piece.Ma_a
    else:
        assert board[9][1] == Piece.Ma_b
        assert board[9][2] == Piece.Sang_b
        assert board[9][6] == Piece.Ma_b
        assert board[9][7] == Piece.Sang_b


def test_inside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.InsideSang),
            get_formation('b', FormationType.InsideSang))
    check_inside_sang('a', j.board)
    check_inside_sang('b', j.board)


def test_outside_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.OutsideSang),
            get_formation('b', FormationType.OutsideSang))
    check_outside_sang('a', j.board)
    check_outside_sang('b', j.board)


def test_inside_sang_x_outside_sang_formation():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.InsideSang),
            get_formation('b', FormationType.OutsideSang))
    check_inside_sang('a', j.board)
    check_outside_sang('b', j.board)


def test_left_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.LeftSang),
            get_formation('b', FormationType.LeftSang))
    check_left_sang('a', j.board)
    check_left_sang('b', j.board)


def test_right_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.RightSang),
            get_formation('b', FormationType.RightSang))
    check_right_sang('a', j.board)
    check_right_sang('b', j.board)


def test_left_sang_x_right_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.LeftSang),
            get_formation('b', FormationType.RightSang))
    check_left_sang('a', j.board)
    check_right_sang('b', j.board)


def test_right_sang_x_left_sang_formation_both():
    j = janggi.Janggi(None)
    j.reset(get_formation('a', FormationType.RightSang),
            get_formation('b', FormationType.LeftSang))
    check_right_sang('a', j.board)
    check_left_sang('b', j.board)
