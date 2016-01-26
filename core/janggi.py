#-*- encoding: utf-8 -*-

"""
    0: 비어있음
    1: ...
    2: ...
    
"""
NAMES = [u'__', u'Kung-a', u'Cha-a', u'Po-a', u'Ma-a', u'Sang-a', u'Byung-a', u'Sa-a', u'Kung-b', u'Cha-b', u'Po-b', u'Ma-b', u'Sang-b', u'Sa-b', u'Jol-b']   # 나중에 추가
assert(len(NAMES) == 7 + 7 + 1)

def code2name(c):
    ret = "[%7s]" % NAMES[c]
    return ret

class Janggi(object):
    def __init__(self):
        self.board = [[0]*9 for _ in range(10)]

    def __repr__(self):
        return '\n'.join(' '.join(map(code2name, row)) for row in self.board)

if '__main__' == __name__:
    janggi = Janggi()
    print(janggi)
    print()
    janggi.board[3][4] = 3
    print(janggi)
