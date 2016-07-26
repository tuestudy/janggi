from data import (
    NUM_ROW, NUM_COL,
    is_valid_coordinates, MOVES,
    Piece, PieceType,
)
import math

# 판이 비어있다고 가정하고, 현재 위치와 기물을 받아서 다음에 갈 수 있는 위치 목록을 리턴

diagonal_moves = {
    (0, 3): [[(1, 4), (2, 5)]],
    (0, 5): [[(1, 4), (2, 3)]],
    (1, 4): [[(0, 3)], [(0, 5)], [(2, 3)], [(2, 5)]],
    (2, 3): [[(1, 4), (0, 5)]],
    (2, 5): [[(1, 4), (0, 3)]],

    (7, 3): [[(8, 4), (9, 5)]],
    (7, 5): [[(8, 4), (9, 3)]],
    (8, 4): [[(7, 3)], [(7, 5)], [(9, 3)], [(9, 5)]],
    (9, 3): [[(8, 4), (7, 5)]],
    (9, 5): [[(8, 4), (7, 3)]],
}


def sorted_coord(coords, origin):
    def distance(dest):
        return math.hypot(origin[0] - dest[0], origin[1] - dest[1])
    return sorted(coords, key=distance)


def is_enemy(board, r, c, code):
    return code.team != board[r][c].team


def is_possible(board, r, c, code):
    return board[r][c] == Piece.Empty or is_enemy(board, r, c, code)


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
            if board[r][c]:
                break


@next_candidates_for(PieceType.Ma, PieceType.Sang)
def ma_sang(board, current_row, current_col, code, coords):
    step = 0
    if code.piece_type == PieceType.Ma:
        step = 2
    elif code.piece_type == PieceType.Sang:
        step = 3

    for r, c in coords:
        ri = 1 if r < current_row else -1
        ci = 1 if c < current_col else -1
        ok = True
        for i in range(0, step):
            if i != 0 and board[r + ri * i][c + ci * i]:
                ok = False
            elif not is_possible(board, r + ri * i, c + ci * i, code):
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
    for r, c in coords:
        if is_possible(board, r, c, code):
            yield r, c


@next_candidates_for(PieceType.Jol)
def byung(board, current_row, current_col, code, coords):
    dmoves = []
    if code == Piece.Jol_a:
        dmoves = [xs[0] for xs in
                  diagonal_moves.get((current_row, current_col), ())
                  if xs[0][0] >= current_row]
    elif code == Piece.Jol_b:
        dmoves = [xs[0] for xs in
                  diagonal_moves.get((current_row, current_col), ())
                  if xs[0][0] <= current_row]

    for r, c in coords + dmoves:
        if is_possible(board, r, c, code):
            yield r, c


def next_coordinates(board, current_row, current_col, code):
    coords = sorted_coord(
        next_possible_coordinates(board, current_row, current_col, code),
        (current_row, current_col))
    f = coordinates_funcs[code.piece_type]
    return list(f(board, current_row, current_col, code, coords))


def next_possible_coordinates(board, current_row, current_col, code):
    assert is_valid_coordinates(current_row, current_col)
    if code.piece_type == PieceType.Cha:
        return cha_next_possible_coordinates(current_row, current_col)
    elif code.piece_type == PieceType.Po:
        return po_next_possible_coordinates(board, current_row, current_col)
    else:
        return item_next_possible_coordinates(
            code, current_row, current_col)


def cha_next_possible_coordinates(row, col):
    for r in range(NUM_ROW):
        if r != row:
            yield r, col
    for c in range(NUM_COL):
        if c != col:
            yield row, c
    for xs in diagonal_moves.get((row, col), ()):
        for r, c in xs:
            yield r, c


def po_next_possible_coordinates(board, row, col):
    def _isPo(code):
        return code and code.piece_type == PieceType.Po

    blocked = False
    for r in range(row + 1, NUM_ROW):
        if _isPo(board[r][col]):
            break
        if not blocked and board[r][col]:
            blocked = True
            continue
        if blocked:
            yield r, col
            if board[r][col]:
                break

    blocked = False
    for r in range(row - 1, -1, -1):
        if _isPo(board[r][col]):
            break
        if not blocked and board[r][col]:
            blocked = True
            continue
        if blocked:
            yield r, col
            if board[r][col]:
                break

    blocked = False
    for c in range(col + 1, NUM_COL):
        if _isPo(board[row][c]):
            break
        if not blocked and board[row][c]:
            blocked = True
            continue
        if blocked:
            yield row, c
            if board[row][c]:
                break

    blocked = False
    for c in range(col - 1, -1, -1):
        if _isPo(board[row][c]):
            break
        if not blocked and board[row][c]:
            blocked = True
            continue
        if blocked:
            yield row, c
            if board[row][c]:
                break

    for xs in diagonal_moves.get((row, col), ()):
        blocked = False
        for r, c in xs:
            if _isPo(board[r][c]):
                break
            if not blocked and board[r][c]:
                blocked = True
                continue
            if blocked:
                yield r, c
                if board[r][c]:
                    break


def item_next_possible_coordinates(piece, row, col):
    moves = MOVES.get(piece) or MOVES.get(piece.piece_type)
    for r, c in moves:
        if is_valid_coordinates(row + r, col + c):
            yield row + r, col + c


def update_possible_coordinates(board, name, row, col, code):
    print("{0} can go to those coordinates from {1}, {2}: ".format(
        name, row, col
    ))
    for r, c in next_possible_coordinates(board, row, col, code):
        board[r][c] = 100
