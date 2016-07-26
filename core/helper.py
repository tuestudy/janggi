from data import code2name


def board_state(board):
    return 'A\n' + '\n'.join(
        ' '.join(map(lambda c: '[%7s]' % code2name(c), row)) for row in board
    ) + '\nB\n'
