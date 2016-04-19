import janggi


def test_initial_board():
    j = janggi.Janggi()
    assert len(j.board) == 10
    assert all(row == [0] * 9 for row in j.board)
