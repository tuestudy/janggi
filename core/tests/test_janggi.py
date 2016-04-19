import janggi


def test_initial_board():
    j = janggi.Janggi()
    assert len(j.board) == 10
    assert all(row == [0] * 9 for row in j.board)
    assert j.on_changed == None

def test_initial_board_with_change_callback():
    def change_callback(board):
        assert True
    j = janggi.Janggi(change_callback)
    j.reset()
    assert len(j.board) == 10
    assert j.on_changed == change_callback
