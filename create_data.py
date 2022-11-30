import math
from general import *
from network import *
from readwrite import *

depth = 1
board = [2,2,0,0,2,0,0,0,0]

save_board = board.copy()

# get a string representing the board and best move in the training data format
def get_pair(board):
    data = ""
    depth = 0
    for i in board:
        data += str(i)
        if i == 0:
            depth += 1
    move = best_move(depth, 2, board)
    if move == -1:
        data += str(avail_moves(board)[0])
    else:
        data += str(move)
    return data

# go through all possible games from the starting board, and return a list of board + best move pairs
def all_combos(depth, mover, board):
    situations = []
    save_board = board.copy()

    if depth > 0:
        for move in avail_moves(board):
            board[move] = mover
            if check_end(board) != 0 and mover == 2:
                situation = get_pair(save_board)
                if situation not in situations:
                    situations.append(situation)
            elif depth > 1:
                newmover = change_turn(mover)
                new_situations = all_combos(depth - 1, newmover, board)
                for situation in new_situations:
                    if situation not in situations:
                        situations.append(situation)
            board = save_board.copy()
    return situations

def main():
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    situations = all_combos(9, 2, board)
    write_situations(situations)

main()