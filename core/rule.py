#-*- encoding: utf-8 -*-
from data import code2name, name2code, MAX_ROW, MAX_COL, \
        is_valid_code, is_valid_coordinates, MOVES
from helper import create_empty_board, board_state

# 판이 비어있다고 가정하고, 현재 위치와 기물을 받아서 다음에 갈 수 있는 위치 목록을 리턴
def next_possible_coordinates(current_row, current_col, code):
    assert(is_valid_coordinates(current_row, current_col))
    name = code2name(code)
    if name.startswith('Cha'):
        return cha_next_possible_coordinates(current_row, current_col)
    elif name.startswith('Po'):
        return po_next_possible_coordinates(current_row, current_col)
    else:
        return item_next_possible_coordinates(name, current_row, current_col)

    return []

def cha_next_possible_coordinates(row, col):
    candidates = []
    for r in range(0, MAX_ROW+1):
        if r != row:
            candidates.append( (r, col) )
    for c in range(0, MAX_COL+1):
        if c != col:
            candidates.append( (row, c) )
    return candidates

def po_next_possible_coordinates(row, col):
    candidates = []
    for r in range(0, MAX_ROW+1):
        if abs(row-r) > 1:
            candidates.append( (r, col) )
    for c in range(0, MAX_COL+1):
        if abs(col-c) > 1:
            candidates.append( (row, c) )
    return candidates

def item_next_possible_coordinates(name, row, col):
    candidates = []
    for r, c in MOVES[name]:
        candidates.append((row + r, col + c))
    return candidates 

if __name__ == '__main__':
    from helper import create_empty_board
    cha_code = name2code('Cha-a')
    board = create_empty_board()
    board[1][1] = cha_code
    print("Cha can go to those coordinates from 1, 1: ")
    for r, c in next_possible_coordinates(1, 1, cha_code):
        board[r][c] = 100
    print(board_state(board))

    po_code = name2code('Po-a')
    board = create_empty_board()
    board[2][2] = po_code
    print("Po can go to those coordinates from 2, 2: ")
    for r, c in next_possible_coordinates(2, 2, po_code):
        board[r][c] = 100
    print(board_state(board))

    jol_code = name2code('Jol-b')
    board = create_empty_board()
    board[2][2] = jol_code
    print("Jol-b can go to those coordinates from 2, 2: ")
    for r, c in next_possible_coordinates(2, 2, jol_code):
        board[r][c] = 100
    print(board_state(board))

    byung_code = name2code('Byung-a')
    board = create_empty_board()
    board[2][2] = byung_code
    print("Byung-a can go to those coordinates from 2, 2: ")
    for r, c in next_possible_coordinates(2, 2, byung_code):
        board[r][c] = 100
    print(board_state(board))
