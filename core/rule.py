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
    for r, c in MOVES[name.split('-')[0]]:
        if is_valid_coordinates(row + r, col + c):
            candidates.append((row + r, col + c))
    return candidates 

def update_possible_coordinates(board, name, row, col, code):
    print("{0} can go to those coordinates from {1}, {2}: ".format(name, row, col))
    for r, c in next_possible_coordinates(row, col, code):
        board[r][c] = 100

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
    board[0][6] = sang_b_code
    board[9][2] = sang_a_code
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
