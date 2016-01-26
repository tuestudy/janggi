#-*- encoding: utf-8 -*-

"""
    0: 비어있음
    1: ...
    2: ...
    
"""
NAMES = [u'__', u'Kung-a', u'Cha-a', u'Po-a', u'Ma-a', u'Sang-a', u'Byung-a', u'Sa-a', u'Kung-b', u'Cha-b', u'Po-b', u'Ma-b', u'Sang-b', u'Sa-b', u'Jol-b']   # 나중에 추가
#         0     1          2         3        4        5          6           7        8          9         10       11       12         13       14
assert(len(NAMES) == 7 + 7 + 1)

A_INITIAL_STATE = [
        (0, 0, 2),
        (0, 1, 4),
        (0, 2, 5),
        (0, 3, 7),
        (0, 5, 7),
        (0, 6, 5),
        (0, 7, 4),
        (0, 8, 2),
        (1, 4, 1),
        (2, 1, 3),
        (2, 7, 3),
        (3, 0, 6),
        (3, 2, 6),
        (3, 4, 6),
        (3, 6, 6),
        (3, 8, 6),
]

B_INITIAL_STATE = [
        (9, 0, 9),
        (9, 1, 12),
        (9, 2, 11),
        (9, 3, 13),
        (9, 5, 13),
        (9, 6, 11),
        (9, 7, 12),
        (9, 8, 9),
        (8, 4, 8),
        (7, 1, 10),
        (7, 7, 10),
        (6, 0, 14),
        (6, 2, 14),
        (6, 4, 14),
        (6, 6, 14),
        (6, 8, 14),
]

def code2name(c):
    ret = "[%7s]" % NAMES[c]
    return ret

class Janggi(object):
    def __init__(self):
        self.board = [[0]*9 for _ in range(10)]

    def __repr__(self):
        return 'A\n' + '\n'.join(' '.join(map(code2name, row)) for row in self.board) + '\nB\n'

    def reset(self):
        self.board = [[0]*9 for _ in range(10)]
        for row, col, code in A_INITIAL_STATE+B_INITIAL_STATE:
            self.board[row][col] = code

if '__main__' == __name__:
    janggi = Janggi()
    janggi.reset()
    print(janggi)
