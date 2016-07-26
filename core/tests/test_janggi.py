# coding: utf-8
from unittest.mock import Mock

import janggi
from formation import get_formation
from data import Piece, NUM_ROW, NUM_COL


def test_initial_board():
    j = janggi.Janggi()
    assert len(j.board) == NUM_ROW
    assert all(row == [Piece.Empty] * NUM_COL for row in j.board)
    assert j.on_changed is None


def test_initial_board_with_change_callback():
    def change_callback(board):
        assert True
    j = janggi.Janggi(change_callback)
    j.reset(get_formation('a'), get_formation('b'))
    assert len(j.board) == NUM_ROW
    assert j.on_changed == change_callback


def test_turn():
    j = janggi.Janggi()
    assert j.turn == 'b'  # 楚
    assert not j.can_move(Piece.Cha_a)
    assert j.can_move(Piece.Cha_b)

    j.change_turn()
    assert j.turn == 'a'  # 漢
    assert j.can_move(Piece.Cha_a)
    assert not j.can_move(Piece.Cha_b)


def test_score():
    j = janggi.Janggi()
    j.reset(get_formation('a'), get_formation('b'))
    assert j.score('a') == 72 + 1.5
    assert j.score('b') == 72


def test_gameover_callback():
    gameover_callback = Mock()
    j = janggi.Janggi(gameover_callback=gameover_callback)
    j.board[1][4] = Piece.Kung_a
    j.board[2][4] = Piece.Jol_b
    j.move((2, 4), (1, 4))
    assert gameover_callback.called
    gameover_callback.assert_called_with((1, 4), 'b')


def test_gameover_callback_shoult_not_be_called_unless_game_is_over():
    gameover_callback = Mock()
    j = janggi.Janggi(gameover_callback=gameover_callback)
    j.board[1][4] = Piece.Kung_a
    j.board[2][4] = Piece.Jol_b
    j.move((2, 4), (2, 5))
    assert not gameover_callback.called
