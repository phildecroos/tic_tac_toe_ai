import math
from general import *
from network import *
from readwrite import *

def possibilities(depth, board):
    count = 0
    for i in range(9):
        if board[i] == 0:
            count += 1
    cases = count
    for i in range(count):
        if i < depth - 1:
            count -= 1
            cases *= count
    return cases

def get_wins(depth, mover, board):
    wins = 0
    save_board = board.copy()

    if depth > 0:
        for move in avail_moves(board):
            board[move] = mover
            if check_end(board) == 2:
                wins += 1
                if depth > 1:
                    wins += possibilities(depth - 1, board)
            elif check_end(board) == 0 and depth > 1:
                if mover == 2:
                    newmover = 1
                else:
                    newmover = 2
                wins += get_wins(depth - 1, newmover, board)

            board = save_board
            save_board = board.copy()

    return wins

print(get_wins(3, 2, [2,2,0,0,2,0,0,0,0]))