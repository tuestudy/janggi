#-*- encoding: utf-8 -*-
from data import code2name, name2code, MAX_ROW, MAX_COL, \
        is_valid_code, is_valid_coordinates

# 판이 비어있다고 가정하고, 현재 위치와 기물을 받아서 다음에 갈 수 있는 위치 목록을 리턴
def next_possible_coordinates(current_row, current_col, code):
    assert(is_valid_coordinates(current_row, current_col))

    return []

if __name__ == '__main__':
    cha_code = name2code('Cha-a')
    print("Cha can go to those coordinates from 1, 1: ")
    for coord in next_possible_coordinates(1, 1, cha_code):
        print(coord)
