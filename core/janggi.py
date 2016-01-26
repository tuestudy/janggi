#-*- encoding: utf-8 -*-

"""
    0: 비어있음
    1: ...
    2: ...
    
"""
NAMES = ['_']   # 나중에 추가

def code2name(c):
    if c >= len(NAMES): # NAMES 가 다 준비되면 지워도 된다
        return '_'

    return NAMES[c]

class Janggi(object):
    def __init__(self):
        self.board = [[0]*9 for _ in range(10)]

    def __repr__(self):
        return '\n'.join(' '.join(map(lambda x: "%4s" % x, row)) for row in self.board)

if '__main__' == __name__:
    janggi = Janggi()
    print(janggi)
