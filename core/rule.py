from data import (
    code2name, name2code, MAX_ROW, MAX_COL,
    is_valid_coordinates, MOVES,
    PieceType,
)
from helper import create_empty_board, board_state
import math

# 판이 비어있다고 가정하고, 현재 위치와 기물을 받아서 다음에 갈 수 있는 위치 목록을 리턴

diagonal_moves = {
    (0,3): [[(1,4),(2,5)]],
    (0,5): [[(1,4),(2,3)]],
    (1,4): [[(0,3)], [(0,5)], [(2,3)], [(2,5)]],
    (2,3): [[(1,4),(0,5)]],
    (2,5): [[(1,4),(0,3)]],

    (7,3): [[(8,4),(9,5)]],
    (7,5): [[(8,4),(9,3)]],
    (8,4): [[(7,3)], [(7,5)], [(9,3)], [(9,5)]],
    (9,3): [[(8,4),(7,5)]],
    (9,5): [[(8,4),(7,3)]],
}

def sorted_coord(coords, origin):
    def distance(dest):
        return math.hypot(origin[0] - dest[0], origin[1] - dest[1])
    return sorted(coords, key=distance)


def is_enemy(board, r, c, code):
    return code.team != board[r][c].team


def is_possible(board, r, c, code):
    return board[r][c] == 0 or is_enemy(board, r, c, code)


coordinates_funcs = {}


def next_candidates_for(*piece_types):
    def deco(f):
        def wrapper(board, current_row, current_col, code, coords):
            f(board, current_row, current_col, code, coords)
        for piece_type in piece_types:
            coordinates_funcs[piece_type] = f
        return wrapper
    return deco


@next_candidates_for(PieceType.Cha)
def cha(board, current_row, current_col, code, coords):
    r_esc = c_esc = False
    coords = [
        [(i, j) for i, j in coords if i == current_row and j < current_col],
        [(i, j) for i, j in coords if i == current_row and j > current_col],
        [(i, j) for i, j in coords if i > current_row and j == current_col],
        [(i, j) for i, j in coords if i < current_row and j == current_col],
        [(i, j) for i, j in coords if i < current_row and j < current_col],
        [(i, j) for i, j in coords if i < current_row and j > current_col],
        [(i, j) for i, j in coords if i > current_row and j < current_col],
        [(i, j) for i, j in coords if i > current_row and j > current_col],
    ]

    for coord in coords:
        for r, c in coord:
            if is_possible(board, r, c, code):
                yield r, c
            if board[r][c] != 0:
                break


@next_candidates_for(PieceType.Ma)
def ma(board, current_row, current_col, code, coords):
    for r, c in coords:
        ri = 1 if r < current_row else -1
        ci = 1 if c < current_col else -1
        ok = True
        for i in range(0, 2):
            if i != 0 and board[r+ri*i][c+ci*i] != 0:
                ok = False
            elif not is_possible(board, r+ri*i, c+ci*i, code):
                ok = False
        if ok:
            yield r, c


@next_candidates_for(PieceType.Sang)
def sang(board, current_row, current_col, code, coords):
    for r, c in coords:
        ri = 1 if r < current_row else -1
        ci = 1 if c < current_col else -1
        ok = True
        for i in range(0, 3):
            if i != 0 and board[r+ri*i][c+ci*i] != 0:
                ok = False
            elif not is_possible(board, r+ri*i, c+ci*i, code):
                ok = False
        if ok:
            yield r, c


@next_candidates_for(PieceType.Sa, PieceType.Kung)
def kung(board, current_row, current_col, code, coords):
    dmoves = [xs[0] for xs in
              diagonal_moves.get((current_row, current_col), ())]
    for r, c in coords:
        if 2 < r < 7:
            continue
        if not (3 <= c <= 5):
            continue
        if is_possible(board, r, c, code):
            if r == current_row or c == current_col or (r, c) in dmoves:
                yield r, c


@next_candidates_for(PieceType.Po)
def po(board, current_row, current_col, code, coords):
    yield from coords


@next_candidates_for(PieceType.Byung, PieceType.Jol)
def byung(board, current_row, current_col, code, coords):
    for r, c in coords:
        if is_possible(board, r, c, code):
            yield r, c


def next_coordinates(board, current_row, current_col, code):
    coords = sorted_coord(
        next_possible_coordinates(board, current_row, current_col, code),
        (current_row, current_col))
    f = coordinates_funcs[code.piece_type]
    return list(f(board, current_row, current_col, code, coords))


def next_possible_coordinates(board, current_row, current_col, code):
    assert(is_valid_coordinates(current_row, current_col))
    name = code2name(code)
    if name.startswith('Cha'):
        return cha_next_possible_coordinates(current_row, current_col)
    elif name.startswith('Po'):
        return po_next_possible_coordinates(board, current_row, current_col)
    else:
        return item_next_possible_coordinates(name, current_row, current_col)


def cha_next_possible_coordinates(row, col):
    for r in range(0, MAX_ROW+1):
        if r != row:
            yield r, col
    for c in range(0, MAX_COL+1):
        if c != col:
            yield row, c
    for xs in diagonal_moves.get((row, col), ()):
        for r, c in xs:
            yield r, c


def po_next_possible_coordinates(board, row, col):
    def _isPo(code):
        return code2name(code).startswith('Po')

    blocked = False
    for r in range(row+1, MAX_ROW+1):
        if _isPo(board[r][col]):
            break
        if not blocked and board[r][col] != 0:
            blocked = True
            continue
        if blocked:
            yield r, col
            if board[r][col] != 0:
                break

    blocked = False
    for r in range(row-1, 0-1, -1):
        if _isPo(board[r][col]):
            break
        if not blocked and board[r][col] != 0:
            blocked = True
            continue
        if blocked:
            yield r, col
            if board[r][col] != 0:
                break

    blocked = False
    for c in range(col+1, MAX_COL+1):
        if _isPo(board[row][c]):
            break
        if not blocked and board[row][c] != 0:
            blocked = True
            continue
        if blocked:
            yield row, c
            if board[row][c] != 0:
                break

    blocked = False
    for c in range(col-1, 0-1, -1):
        if _isPo(board[row][c]):
            break
        if not blocked and board[row][c] != 0:
            blocked = True
            continue
        if blocked:
            yield row, c
            if board[row][c] != 0:
                break

    blocked = False
    for xs in diagonal_moves.get((row, col), ()):
        for r, c in xs:
            if _isPo(board[r][c]):
                break
            if not blocked and board[r][c] != 0:
                blocked = True
                continue
            if blocked:
                yield r, c
                if board[r][c] != 0:
                    break


def item_next_possible_coordinates(name, row, col):
    for r, c in MOVES[name.split('-')[0]]:
        if is_valid_coordinates(row + r, col + c):
            yield row + r, col + c


def update_possible_coordinates(board, name, row, col, code):
    print("{0} can go to those coordinates from {1}, {2}: ".format(
        name, row, col
    ))
    for r, c in next_possible_coordinates(board, row, col, code):
        board[r][c] = 100

if __name__ == '__main__':
    cha_code = name2code('Cha-a')
    board = create_empty_board()
    board[1][1] = cha_code
    print("Cha can go to those coordinates from 1, 1: ")
    for r, c in next_possible_coordinates(board, 1, 1, cha_code):
        board[r][c] = 100
    print(board_state(board))

    po_code = name2code('Po-a')
    board = create_empty_board()
    board[2][2] = po_code
    print("Po can go to those coordinates from 2, 2: ")
    for r, c in next_possible_coordinates(board, 2, 2, po_code):
        board[r][c] = 100
    print(board_state(board))

    byung_code = name2code('Byung-a')
    jol_code = name2code('Jol-b')
    board = create_empty_board()
    board[2][2] = byung_code
    board[6][2] = jol_code
    update_possible_coordinates(board, 'Byung-a', 2, 2, byung_code)
    update_possible_coordinates(board, 'Jol-b', 6, 2, jol_code)
    print(board_state(board))

    ma_a_code = name2code('Ma-a')
    ma_b_code = name2code('Ma-b')
    board = create_empty_board()
    board[0][1] = ma_a_code
    board[0][7] = ma_a_code
    board[9][1] = ma_b_code
    board[9][7] = ma_b_code
    update_possible_coordinates(board, 'Ma-a', 0, 1, ma_a_code)
    update_possible_coordinates(board, 'Ma-a', 0, 7, ma_a_code)
    update_possible_coordinates(board, 'Ma-a', 9, 1, ma_b_code)
    update_possible_coordinates(board, 'Ma-a', 9, 7, ma_b_code)
    print(board_state(board))

    sang_a_code = name2code('Sang-a')
    sang_b_code = name2code('Sang-b')
    board = create_empty_board()
    board[0][2] = sang_a_code
    board[0][6] = sang_a_code
    board[9][2] = sang_b_code
    board[9][6] = sang_b_code
    update_possible_coordinates(board, 'Sang-a', 0, 2, sang_a_code)
    update_possible_coordinates(board, 'Sang-a', 0, 6, sang_a_code)
    update_possible_coordinates(board, 'Sang-a', 9, 2, sang_b_code)
    update_possible_coordinates(board, 'Sang-a', 9, 6, sang_b_code)
    print(board_state(board))

    kung_a_code = name2code('Kung-a')
    kung_b_code = name2code('Kung-b')
    board = create_empty_board()
    board[1][4] = kung_a_code
    board[8][4] = kung_b_code
    update_possible_coordinates(board, 'Kung-a', 1, 4, kung_a_code)
    update_possible_coordinates(board, 'Kung-b', 8, 4, kung_b_code)
    print(board_state(board))

    sa_a_code = name2code('Sa-a')
    sa_b_code = name2code('Sa-b')
    board = create_empty_board()
    board[1][4] = sa_a_code
    board[8][4] = sa_b_code
    update_possible_coordinates(board, 'Sa-a', 1, 4, sa_a_code)
    update_possible_coordinates(board, 'Sa-b', 8, 4, sa_b_code)
    print(board_state(board))
