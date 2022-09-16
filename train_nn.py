import os
import random
from os.path import exists

clear = lambda: os.system('cls')
clear()
print("starting...")

"""
for consistency, the neural network always plays as O

tic tac toe board format:

val: 0 = blank, 1 = X, -1 = O
[<val>, <val>, <val>, <val>, <val>, <val>, <val>, <val>, <val>]

network_properties.txt format (each value on it's own line with a \n at the end):

weight1
bias1
weight2
bias2
...

"""

# read weights and biases from saved txt file
props = []

with open("network_properties.txt", "r") as doc:
    for line in doc:
        props.append(line[0:-1])

weights = [[], [], [], [], [], [], [], [], []]
biases = [[], [], [], [], [], [], [], [], []]

j = -1
for i in range(162):
    if i % 18 == 0:
        j += 1
    if i % 2 == 0:
        weights[j].append(float(props[i]))
    else:
        biases[j].append(float(props[i]))

# def function to find free moves given a board
def free_moves(board):
    output = []

    for i in range(9):
        if board[i] == 0:
            output.append(i)
    
    return output

# def function to compute the network outputs from a tic tac toe board
def find_move(board):
    outputs = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    for i in range(9):
        for j in range(9):
            outputs[i] += board[i] * weights[j][i] + biases[j][i]

    avail = free_moves(board)

    for i in range(9):
        max_index = outputs.index(max(outputs))

        if max_index in avail:
            return max_index
        else:
            outputs[max_index] = -1.0

# def function that chooses a random cell from the available ones
def rand_move(board):
    return random.choice(tuple(free_moves(board)))
    # avail = free_moves(board)
    # move = avail[random.randint(0, len(avail) - 1)]
    # return move

# def function that checks if there is a winner
def check_win(board):
    winner = 0

    if board[0] == board[1] and board[1] == board[2] and board[2] != 0:
        winner = board[0]
    if board[3] == board[4] and board[4] == board[5] and board[5] != 0:
        winner = board[3]
    if board[6] == board[7] and board[7] == board[8] and board[8] != 0:
        winner = board[6]
    if board[0] == board[3] and board[3] == board[6] and board[6] != 0:
        winner = board[0]
    if board[1] == board[4] and board[4] == board[7] and board[7] != 0:
        winner = board[1]
    if board[2] == board[5] and board[5] == board[8] and board[8] != 0:
        winner = board[2]
    if board[0] == board[4] and board[4] == board[8] and board[8] != 0:
        winner = board[0]
    if board[2] == board[4] and board[4] == board[6] and board[6] != 0:
        winner = board[2]

    # check if there is no winner but all 9 squares are full
    if winner != 0:
        return winner
    
    for i in board:
        if i == 0:
            return 0
    return 2

# def function that prints a readable tic tac toe board
def print_board(board):
    for i in range(9):
        if i % 3 == 0:
            print("")

        if board[i] == 0:
            print("[ ]", end="")
        elif board[i] == -1:
            print("[O]", end="")
        elif board[i] == 1:
            print("[X]", end="")

# train the model against a bot that does random moves for num_games games
num_games = 10000000
wins = 0
draws = 0
losses = 0

# training parameters
test_rate = 0.1 # the % it will change randomly selected values by during each test

for i in range(num_games):
    if i % (num_games / 100) == 0:
        clear()
        print("games played: " + str(i))

    # change a random value for the test
    posneg = random.randint(0,1) * 2 - 1 # will randomly be 1 or -1
    test_type = random.randint(0,1)
    test_row = random.randint(0,8)
    test_col = random.randint(0,8)
    if test_type:
        test_change = test_rate * posneg * weights[test_row][test_col]
        weights[test_row][test_col] += test_change
    else:
        test_change = test_rate * posneg * biases[test_row][test_col]
        biases[test_row][test_col] += test_change

    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # randomly determine who goes first
    curr_player = random.randint(0, 1)

    while check_win(board) == 0:
        if curr_player % 2 == 0:
            board[find_move(board)] = -1
        else:
            board[rand_move(board)] = 1
        curr_player += 1

    # edit the model based on the outcome of the game
    outcome = check_win(board)
    # if loss, revert the change back
    if outcome == 1:
        losses += 1
        if test_type:
            weights[test_row][test_col] -= test_change
        else:
            biases[test_row][test_col] -= test_change
    # if win or draw, keep the change the way it is
    elif outcome == -1:
        wins += 1
    else:
        draws += 1

#print_board(board)

# write new weights and biases to save file
j = -1
with open("network_properties.txt", "w") as doc:
    for j in range(9):
        for i in range(9):
            doc.write(str(weights[j][i]) + "\n")
            doc.write(str(biases[j][i]) + "\n")

clear()
print("games played: " + str(num_games))
print("wins: " + str(wins))
print("draws: " + str(draws))
print("losses: " + str(losses))