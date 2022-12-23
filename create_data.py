from general import *
from network import *
from readwrite import *

# get a string representing the board and best move in the training data format
def get_pair(board):
    data = ""
    for i in board:
        data += str(i)
    data += str(best_move(board.count(0), -1, board))
    return data

# go through all possible games from the starting board, and return best moves
def all_combos(depth, mover, board):
    situations = []
    if check_end(board) != 0:
        return situations

    # get the best move for the current board if it is the ai's turn
    local_board = board.copy()
    if depth > 0 and mover == -1:
        situation = get_pair(local_board)
        if situation not in situations:
            situations.append(situation)

    # recursively get the best moves for subsequent boards
    if depth > 1:
        # since the ai can be assumed to always do the best move
        # only check boards where the ai has previously done the best moves
        # but check boards for all possible moves from the opponent
        if mover == -1:
            local_board[best_move(board.count(0), -1, board)] = -1
            new_situations = all_combos(depth - 1, 1, local_board)
            for situation in new_situations:
                if situation not in situations:
                    situations.append(situation)
        else:
            for move in avail_moves(local_board):
                local_board[move] = 1
                new_situations = all_combos(depth - 1, -1, local_board)
                for situation in new_situations:
                    if situation not in situations:
                        situations.append(situation)
                local_board = board.copy()
    return situations

# generate a dataset of all boards the ai can encounter and their best move
def generate():
    situations = []
    
    board = [0 for i in range(9)]
    for situation in all_combos(9, -1, board):
        if situation not in situations:
            situations.append(situation)
    for situation in all_combos(9, 1, board):
        if situation not in situations:
            situations.append(situation)
    write_situations(situations, "situations_new.txt")

# remove bad data points from the dataset (rn its boards with only one move)
def optimize_data():
    situations = read_situations("situations_new.txt")
    new_situations = []
    for situation in situations:
        if situation[0].count(0) > 1:
            new_situation = ""
            for i in range(9):
                new_situation += str(situation[0][i])
            new_situation += str(situation[1])
            new_situations.append(new_situation)
    write_situations(new_situations, "situations_new.txt")

# check the dataset for bad data (rn its boards with only one move)
def data_quality():
    situations = read_situations("situations_new.txt")
    one_moves = 0
    for situation in situations:
        if situation[0].count(0) == 1:
            one_moves += 1
    print("one move data points: " + str(one_moves))

print("generating data")
generate()
data_quality()
print("optimizing data")
optimize_data()
data_quality()
print("done")