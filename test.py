import random
from general import *
from network import *
from readwrite import *

def random_move(board):
    move = -1
    while move not in avail_moves(board):
        move = random.randint(0, 9)
    return move

def main():
    nodes = generate()
    read_params(nodes, "params_init.txt")

    games = 1000
    wins = 0
    losses = 0
    draws = 0

    for i in range(games):
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        curr_player = random.randint(1, 2)
        while not check_end(board):
            if curr_player == 1:
                board[random_move(board)] = 1
                curr_player = 2
            else:
                board[find_move(nodes, board)] = 2
                curr_player = 1

        result = check_end(board)
        if result == 1:
            losses += 1
        elif result == 2:
            wins += 1
        elif result == -1:
            draws += 1
    
    clear()
    print(str(games) + " games vs random moves")
    print("wins: " + str(wins))
    print("losses: " + str(losses))
    print("draws: " + str(draws))

main()