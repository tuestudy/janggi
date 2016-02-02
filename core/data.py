#-*- encoding: utf-8 -*-

MAX_ROW = 9
MAX_COL = 8

CODE_NAMES = [u'__', u'Kung-a', u'Cha-a', u'Po-a', u'Ma-a', u'Sang-a', u'Byung-a', u'Sa-a', u'Kung-b', u'Cha-b', u'Po-b', u'Ma-b', u'Sang-b', u'Sa-b', u'Jol-b']   # 나중에 추가
#         0     1          2         3        4        5          6           7        8          9         10       11       12         13       14
assert(len(CODE_NAMES) == 7 + 7 + 1)

def is_valid_code(c):
    return 0 <= c < len(CODE_NAMES)
 
def is_valid_coordinates(r, c):
    return 0 <= r <= MAX_ROW and 0 <= c <= MAX_COL

def code2name(c):
    ret = "[%7s]" % CODE_NAMES[c]
    return ret

def name2code(name):
    return CODE_NAMES.index(name)

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

