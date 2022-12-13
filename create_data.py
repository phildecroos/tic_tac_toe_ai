import math
from general import *
from network import *
from readwrite import *

# get a string representing the board and best move in the training data format
def get_pair(board):
    data = ""
    depth = 0
    for i in board:
        data += str(i)
        if i == 0:
            depth += 1
    move = best_move(depth, -1, board)
    if move == -1:
        data += str(avail_moves(board)[0])
    else:
        data += str(move)
    return data

# go through all possible games from the starting board, and return a list of board + best move pairs
def all_combos(depth, mover, board):
    situations = []
    if check_end(board) != 0:
        return situations

    save_board = board.copy()

    if depth > 0:
        for move in avail_moves(board):
            board[move] = mover
            if check_end(board) != 0 and mover == -1:
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

# generate a complete dataset of all boards the ai can encounter and the best move
def generate():
    situations = []
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for situation in all_combos(9, -1, board):
        if situation not in situations:
            situations.append(situation)

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for situation in all_combos(9, 1, board):
        if situation not in situations:
            situations.append(situation)
    write_situations(situations, "situations_new.txt")

# remove situations that have only 1 possible move from dataset
def optimize_data():
    situations = read_situations("situations_new.txt")
    new_situations = []
    for situation in situations:
        new_situation = ""
        zeros = 0
        for i in range(9):
            if situation[0][i] == 0:
                zeros += 1
            new_situation += str(situation[0][i])
        new_situation += str(situation[1])
        if zeros > 1:
            new_situations.append(new_situation)
    write_situations(new_situations, "situations_new.txt")

# check the dataset for bad data (already done games, one move available)
def data_quality():
    situations = read_situations("situations_new.txt")
    for situation in situations:
        zeros = 0
        for i in range(9):
            if situation[0][i] == 0:
                zeros += 1
        if zeros <= 1:
            print(situation)

generate()
print("generated data")
data_quality()
optimize_data()
print("optimized data")
data_quality()